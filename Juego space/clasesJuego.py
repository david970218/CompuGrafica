import pygame
import random

ANCHO=1200
ALTO=600
NEGRO=[0,0,0]
ROJO=[255,0,0]
VERDE=[0,255,0]
AMARILLO=[255,255,0]
BLANCO=[255,255,255]
TIEMPO_DISPARO_ENEMIGO = 60

class sprite(pygame.sprite.Sprite):
    def __init__(self,image, color  , pos , vel):
        pygame.sprite.Sprite.__init__(self)
        self.image= image
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.velx = vel[0]
        self.vely = vel[1]

    def update(self):
        pass

    def get_size(self):
        w = self.rect.width
        h = self.rect.height
        return (w , h)

    def get_pos(self):
        return(self.rect.x , self.rect.y)

class Creator:
    def factory_method(self , args = None):
        pass


class JugadorCreator(Creator):
    def factory_method(self ):
        image = pygame.Surface([ 50 , 50 ])
        color = BLANCO
        pos = [(ANCHO / 2) , (ALTO - 50)]
        vel = (0 , 0)
        return Jugador(image , color , pos , vel)


class EnemigoCreator(Creator):
    def factory_method(self):
        image = pygame.Surface([50 , 50])
        color = VERDE
        x=random.randrange(ANCHO - 50)
        y=random.randrange(50 ,ALTO - 100, 70)
        pos = (x , y)
        vx =random.randrange(9) + 1
        vel = ( vx , 0)
        enemigo = Enemigo(image , color , pos , vel)
        enemigo.set_tmp()
        return enemigo


class BalaCreator(Creator):
    def factory_method(self, pos , vy , color):
        image = pygame.Surface([5 , 15])
        vel = (0 , vy)
        return Bala(image , color , pos , vel)


class Jugador(sprite):
    vidas = 3
    def mover(self , x):
        self.rect.x = x

    def disparo(self):
        x , y = self.get_size()
        xpos , ypos = self.get_pos()
        x /= 2
        x += xpos
        y = ypos
        balaCreator = BalaCreator()
        return balaCreator.factory_method((x,y) , -5 , AMARILLO)

class Bala(sprite):
    pass

class Enemigo(sprite):
    def set_tmp(self):
        self.tmp = random.randrange(60)

    def disparo(self):
        x , y = self.get_size()
        xpos , ypos = self.get_pos()
        x /= 2
        x += xpos
        y = ypos
        balaCreator = BalaCreator()
        return  balaCreator.factory_method((x,y) , 10 , ROJO)


class Juego:
    def __init__(self):
        #Definicion de variables
        self.gameOver = False
        self.ventana=pygame.display.set_mode([ANCHO,ALTO])
        self.jugadores=pygame.sprite.Group()
        self.rivales=pygame.sprite.Group()
        self.jugadorCreator = JugadorCreator()
        self.enemigoCreator = EnemigoCreator()
        self.balas = pygame.sprite.Group()
        self.balasRivales = pygame.sprite.Group()
        self.j= self.jugadorCreator.factory_method()
        self.jugadores.add(self.j)
        n=1
        for i in range(n):
            r = self.enemigoCreator.factory_method()
            self.rivales.add(r)

    def Jugar(self):
        reloj=pygame.time.Clock()
        pause = True
        fin=False
        while not fin:
            #Gestion eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin=True
                if event.type == pygame.MOUSEMOTION:
                    self.j.mover(event.pos[0] - 25)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            pause = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.balas.add(self.j.disparo())
            #Refresco
            self.tick(self.rivales)
            self.disparo_rivales(self.rivales , self.balasRivales)
            self.update(self.balas)
            self.update(self.balasRivales)
            self.update(self.rivales)
            self.ventana.fill(NEGRO)
            self.jugadores.draw(self.ventana)
            self.balas.draw(self.ventana)
            self.balasRivales.draw(self.ventana)
            self.rivales.draw(self.ventana)
            self.colisiones_balas(self.balas, self.rivales)
            self.eliminar_balas(self.balas)
            self.eliminar_balas_rivales(self.balasRivales)
            self.disparo_a_jugador()
            self.fin_de_juego()
            pygame.display.flip()
            reloj.tick(40)
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        fin = True
                        pause = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pause = False
            print self.j.vidas

    def colisiones_balas(self , balas , enemigos):
        ls_col = []
        for bala in balas:
            ls_col = pygame.sprite.spritecollide(bala , enemigos, True)
            if len(ls_col) > 0:
                balas.remove(bala)
        return ls_col

    def eliminar_balas(self , balas):
        for bala in balas:
            if bala.rect.y < 50:
                balas.remove(bala)
        return None

    def update(self , sprites):
        for sprite in sprites:
            if sprite.rect.x + sprite.velx > ANCHO - 50  or sprite.rect.x + sprite.velx < 0:
                sprite.velx *= -1
            sprite.rect.x += sprite.velx
            sprite.rect.y += sprite.vely




    def disparo_rivales(self , enemigos , balas):
        for enemigo in enemigos:
            if enemigo.tmp < 0:
                balas.add(enemigo.disparo())
                enemigo.tmp = TIEMPO_DISPARO_ENEMIGO


    def tick(self , enemigos):
        for enemigo in enemigos:
            enemigo.tmp -= 1


    def eliminar_balas_rivales(self , balas):
        for bala in balas:
            if bala.rect.y > ALTO - 10:
                balas.remove(bala)
        return None

    def disparo_a_jugador(self):
        ls_col = []
        for bala in self.balasRivales:
            ls_col  += pygame.sprite.spritecollide(bala, self.jugadores , False)
            if len(ls_col) > 0:
                self.j.vidas -=1
                self.balasRivales.remove(bala)
        return ls_col

    def fin_de_juego(self):
        if self.j.vidas == 0:
            self.gameOver = True
