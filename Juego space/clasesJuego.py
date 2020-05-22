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
        print self.image.get_rect() , type(self)
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
    def __init__(self):
        self.personajes = pygame.image.load("Sprites/animales.png")

    def cargarAnimales(self ,(x,y) ):
        animal = []
        for i in range(x ,x + 4):
            ls = []
            for j in range(y, y + 3):
                corte = self.personajes.subsurface( j*32 , i*32 , 32 , 32 )
                ls.append(corte)
            animal.append(ls)
        return animal


    def factory_method(self, pos , name):
        image = pygame.Surface([ 32 , 32 ])
        color = None
        vel = (0 , 0)
        jugador = Jugador(image , color , pos , vel)
        if name == "gato":
            jugador.animal = self.cargarAnimales((0,0))
            jugador.setAnim()
        return jugador



class BloqueCreator(Creator):
    def factory_method(self, pos , tam ,  texturas = None , poscorte = None):
        if texturas != None:
            image = texturas.subsurface(poscorte[0] , poscorte[1]  , tam[0] , tam[1])
            color = None
        else:
            image = pygame.Surface(tam)
            color = ROJO
        vel = (0 , 0)
        return Bloque(image , color , pos , vel)

class FondoCreator(Creator):
    def factory_method(self, pos):
        image = pygame.image.load("Mapa/mapa1.png")
        vel = (0 , 0)
        return Fondo(image , None , pos , vel)


class Jugador(sprite):
    abajo = 0
    izquierda = 1
    derecha = 2
    arriba = 3
    dir = 0
    animacion = 1
    animal = None
    vidas = 3

    def mover(self , x):
        self.rect.x = x

    def setAnim(self):
        if self.vely == 0:
            if self.dir == self.arriba:
                self.animacion = 0
            elif self.dir == self.abajo:
                self.animacion = 0
        if self.velx == 0:
            if self.dir == self.izquierda:
                self.animacion = 0
            elif self.dir == self.derecha:
                self.animacion = 0
        if self.animacion == 2:
            self.animacion = 0
        else:
            self.animacion += 1
        self.image = self.animal[self.dir][self.animacion]

class Fondo(sprite):
    pass


class Bloque(sprite):
    pass

class Juego:
    def __init__(self):
        #Definicion de variables
        self.gameOver = False
        self.fondo = FondoCreator().factory_method((0,0))
        self.texturas = pygame.image.load("Fondo/textura.png")
        self.cuadro = self.texturas.subsurface(0,0,32,32)
        self.ventana=pygame.display.set_mode([ANCHO,ALTO])
        self.texturaFondo = pygame.sprite.Group()
        self.bloques = pygame.sprite.Group()
        self.jugadores=pygame.sprite.Group()
        self.jugadorCreator = JugadorCreator()
        self.bloqueCreator = BloqueCreator()
        self.bloque = self.bloqueCreator.factory_method((300,300) , (32 , 32) ,  self.texturas , (0,0)  )
        self.texturaFondo.add(self.fondo)
        self.bloques.add(self.bloque)
        self.j= self.jugadorCreator.factory_method((ANCHO/2 , ALTO/2) , "gato")
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
                    if event.key == pygame.K_UP :
                        self.j.dir = self.j.arriba
                        self.j.vely = -5
                        self.j.velx = 0
                    if event.key == pygame.K_LEFT:
                        self.j.dir = self.j.izquierda
                        self.j.velx  = -5
                        self.j.vely = 0
                    if event.key == pygame.K_RIGHT:
                        self.j.dir = self.j.derecha
                        self.j.velx  = 5
                        self.j.vely = 0
                    if event.key == pygame.K_DOWN:
                        self.j.dir = self.j.abajo
                        self.j.velx  = 0
                        self.j.vely = 5
                    if event.key == pygame.K_SPACE:
                        self.j.velx = 0
                        self.j.vely = 0

            self.ventana.fill(NEGRO)
            #Refresco
            self.ventana.blit(self.cuadro , [0,0])
            self.j.setAnim()
            self.texturaFondo.draw(self.ventana)
            self.bloques.draw(self.ventana)
            self.jugadores.draw(self.ventana)
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
                return 0
            if sprite.rect.y + sprite.vely > ALTO - 50  or sprite.rect.y + sprite.vely < 0:
                return 0
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
