import pygame
import random

#2500 1800

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
        if color != None:
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
    def factory_method(self, pos):
        image = pygame.Surface([ 50 , 50 ])
        color = BLANCO
        vel = (0 , 0)
        return Jugador(image , color , pos , vel)

class BloqueCreator(Creator):
    def factory_method(self, pos , tam):
        image = pygame.Surface(tam)
        color = ROJO
        vel = (0 , 0)
        return Bloque(image , color , pos , vel)

class FondoCreator(Creator):
    def factory_method(self, pos):
        image = pygame.image.load("Fondo/fondo.jpg")
        color = ROJO
        vel = (0 , 0)
        return Fondo(image , None , pos , vel)


class Jugador(sprite):
    vidas = 3
    def mover(self , x):
        self.rect.x = x

class Fondo(sprite):
    pass


class Bloque(sprite):
    pass

class Juego:
    def __init__(self):
        #Definicion de variables
        self.gameOver = False
        self.fondo = FondoCreator().factory_method((0,0))
        self.ventana=pygame.display.set_mode([ANCHO,ALTO])
        self.bloques = pygame.sprite.Group()
        self.jugadores=pygame.sprite.Group()
        self.jugadorCreator = JugadorCreator()
        self.bloqueCreator = BloqueCreator()
        self.bloque = self.bloqueCreator.factory_method((300,300) , (100 , 70))
        self.bloques.add(self.bloque)
        self.j= self.jugadorCreator.factory_method((ANCHO/2 , ALTO/2))
        self.jugadores.add(self.j)

    def Jugar(self):
        reloj=pygame.time.Clock()
        pause = True
        fin=False
        while not fin:
            #Gestion eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            pause = True
                    if event.key == pygame.K_UP:
                        self.j.vely = -5
                        self.j.velx = 0
                    if event.key == pygame.K_LEFT:
                        self.j.velx  = -5
                        self.j.vely = 0
                    if event.key == pygame.K_RIGHT:
                        self.j.velx  = 5
                        self.j.vely = 0
                    if event.key == pygame.K_DOWN:
                        self.j.velx  = 0
                        self.j.vely = 5

            #Refresco
            self.ventana.fill(NEGRO)
            self.fondo.draw(self.ventana)
            self.jugadores.draw(self.ventana)
            self.bloques.draw(self.ventana)
            self.colisiones()
            self.update(self.jugadores)
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



    def update(self , sprites):
        for sprite in sprites:
            if sprite.rect.x + sprite.velx > ANCHO - 50  or sprite.rect.x + sprite.velx < 0:
                sprite.velx *= -1
            if sprite.rect.y + sprite.vely > ALTO - 50  or sprite.rect.y + sprite.vely < 0:
                sprite.vely *= -1
            sprite.rect.x += sprite.velx
            sprite.rect.y += sprite.vely

    def colisiones(self):
        ls_col = []
        for bloque in self.bloques:
            ls_col = pygame.sprite.spritecollide(self.j , self.bloques , False)
            for b in ls_col:
                print len(ls_col)
                if self.j.vely < 0:
                    if self.j.rect.top < b.rect.bottom:
                        self.j.rect.top = b.rect.bottom
                        self.j.vely = 0
                elif self.j.vely > 0:
                        if self.j.rect.bottom > b.rect.top:
                            self.j.rect.bottom = b.rect.top
                            self.j.vely = 0


            ls_col = pygame.sprite.spritecollide(self.j , self.bloques , False)
            for b in ls_col:
                if self.j.velx < 0:
                    if self.j.rect.left < b.rect.right:
                        self.j.rect.left = b.rect.right
                        self.j.velx = 0
                elif self.j.velx > 0:
                    if self.j.rect.right > b.rect.left:
                        self.j.rect.right = b.rect.left
                        self.j.velx = 0
