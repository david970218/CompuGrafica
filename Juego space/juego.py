import pygame
from clasesJuego import *
import random



if __name__ == '__main__':
    pygame.init()
    juego  = Juego()
    #Definicion de variables
    ventana=pygame.display.set_mode([ANCHO,ALTO])
    jugadores=pygame.sprite.Group()
    rivales=pygame.sprite.Group()
    jugadorCreator = JugadorCreator()
    enemigoCreator = EnemigoCreator()
    balas = pygame.sprite.Group()
    balasRivales = pygame.sprite.Group()
    j= jugadorCreator.factory_method()
    jugadores.add(j)
    n=1
    for i in range(n):
        r = enemigoCreator.factory_method()
        rivales.add(r)

    reloj=pygame.time.Clock()
    pause = True
    fin=False
    while not fin:
        #Gestion eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.MOUSEMOTION:
                j.mover(event.pos[0] - 25)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        pause = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                balas.add(j.disparo())
        #Refresco
        juego.tick(rivales)
        juego.disparo_rivales(rivales , balasRivales)
        juego.update(balas)
        juego.update(balasRivales)
        juego.update(rivales)
        ventana.fill(NEGRO)
        jugadores.draw(ventana)
        balas.draw(ventana)
        balasRivales.draw(ventana)
        rivales.draw(ventana)
        juego.colisiones_balas(balas, rivales)
        juego.eliminar_balas(balas)
        juego.eliminar_balas_rivales(balasRivales)
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
        
        