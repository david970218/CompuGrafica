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
    def __init__(self):
        self.personaje = pygame.image.load("Sprites/ken.png")

    def cargarAnimaciones(self):
        animaciones = []
        for i in range(0 , 10):
            animacion = []
            for j in range(0 , 7):
                corte = self.personaje.subsurface( j*52 , i*61 , 52 , 61 )
                animacion.append(corte)
            animaciones.append(animacion)
        return animaciones


    def factory_method(self, pos):
        image = pygame.Surface([ 32 , 32 ])
        color = None
        vel = (0 , 0)
        jugador = ken(image , color , pos , vel)
        jugador.animaciones = self.cargarAnimaciones()
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
    pass

class ken(Jugador):
    anim = 1
    cont = 0
    poder = 0
    defensa = 1
    punio = 2
    caminar = 3
    patada = 6
    patadaGiratoria = 7
    salto = 8
    agacharse = 9
    animaciones = None

    def setAnim(self):
        if self.anim == self.agacharse:
            self.cont = 0

        self.image = self.animaciones[self.anim][self.cont]
        if self.anim == self.poder:
            if self.cont == 3:
                self.cont = 0
                self.anim = self.defensa
        elif self.anim == self.defensa:
            if self.cont == 3:
                self.cont = 0
        elif self.anim == self.punio:
            if self.cont == 2:
                self.cont = 0
                self.anim = self.defensa
        elif self.anim == self.caminar:
            if self.cont == 4:
                self.cont = 0
        elif self.anim == self.patada:
            if self.cont == 4:
                self.cont = 0
                self.anim = self.defensa
        elif self.anim == self.patadaGiratoria:
            if self.cont == 4:
                self.cont = 0
                self.anim = self.defensa
        elif self.anim == self.salto:
            if self.cont == 6:
                self.cont = 0
                self.anim = self.defensa
        self.cont += 1






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
        self.reloj=pygame.time.Clock()
        self.texturaFondo.add(self.fondo)
        self.bloques.add(self.bloque)
        self.j= self.jugadorCreator.factory_method((ANCHO/2 , ALTO/2))
        self.jugadores.add(self.j)

    def Jugar(self):
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
                        self.j.anim = self.j.salto
                        self.j.vely = 0
                        self.j.velx = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.j.anim = self.j.caminar
                        self.j.cont = 0
                        self.j.velx  = -5
                        if event.key == pygame.K_RIGHT:
                            self.j.velx = 5
                        self.j.vely = 0
                        fin2 = False
                        while not fin2:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    self.j.anim = self.j.salto
                                if event.type == pygame.KEYUP and event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                                    fin2=True
                            if self.j.anim == self.j.defensa:
                                self.j.anim =  self.j.caminar
                            self.refresco()
                        self.j.cont = 0
                        self.j.anim = self.j.defensa
                        self.j.velx  = 0
                    if event.key == pygame.K_DOWN:
                        self.j.anim = self.j.agacharse
                        fin2 = False
                        while not fin2:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYUP:
                                    fin2=True
                            self.refresco()
                        self.j.anim = self.j.defensa

                    if event.key == pygame.K_SPACE:
                        self.j.velx = 0
                        self.j.vely = 0


            #Refresco
            self.refresco()

            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        fin = True
                        pause = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pause = False

    def refresco(self):
        self.ventana.fill(NEGRO)
        self.ventana.blit(self.cuadro , [0,0])
        self.j.setAnim()
        self.texturaFondo.draw(self.ventana)
        self.bloques.draw(self.ventana)
        self.jugadores.draw(self.ventana)
        self.colisiones()
        self.update(self.jugadores)
        pygame.display.flip()
        self.reloj.tick(10)


    def update(self , sprites):
        for sprite in sprites:
            if sprite.rect.x + sprite.velx > ANCHO - 50  or sprite.rect.x + sprite.velx < 0:
                pass
            if sprite.rect.y + sprite.vely > ALTO - 50  or sprite.rect.y + sprite.vely < 0:
                pass
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
