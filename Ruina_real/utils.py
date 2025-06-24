import pygame
import time
import random
import sys
from config import pantalla, reloj, ANCHO, TAMAÑO_FUENTE, AMARILLO, BLANCO



# muestra la accion que realizan los personajes y muestra el tiempo que dura el mensaje
mensaje_combate = ""                                                                         
tiempo_mensaje = 0   
#------------------------------PROBABILIDAD ESQUIVE-----------------------------------#
def esquiva(probabilidad_esquive):                                                          # probabilidad de esquivar
    return random.randint(1, 100) > probabilidad_esquive
#------------------------------PROBABILIDAD ESQUIVE-----------------------------------#


#-------------------------------MOSTRAR MENSAJE---------------------------------------#
def mostrar_mensaje_superior(texto, duracion=5):
    global mensaje_combate, tiempo_mensaje
    mensaje_combate = texto
    tiempo_mensaje = time.time() + duracion

def dibujar_mensaje():
    if mensaje_combate and time.time() < tiempo_mensaje:
        fuente_mensaje = pygame.font.SysFont("GODOFWAR", TAMAÑO_FUENTE)
        texto_render = fuente_mensaje.render(mensaje_combate, True, (AMARILLO))
        pantalla.blit(texto_render, (ANCHO // 2 - texto_render.get_width() // 2, 20))   
#-------------------------------MOSTRAR MENSAJE---------------------------------------#


#---------------------------ELEGIR CURARSE O ATACAR-----------------------------------#
def esperar_eleccion_jugador():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    return "atacar"
                elif evento.key == pygame.K_c:
                    return "curar"
#---------------------------ELEGIR CURARSE O ATACAR-----------------------------------#


#----------------------------ANIMACION DE CURACION------------------------------------#
def animacion_curacion(personaje, cantidad, pantalla, fondo, jugador=None, aliado=None, enemigo=None, color=(BLANCO)):
    fuente_curacion = pygame.font.SysFont("GODOFWAR", TAMAÑO_FUENTE, True)
    texto = fuente_curacion.render(f"+{cantidad}", True, color)
    x, y = personaje.x, personaje.y
    desplazamiento = 0
    sonido_curacion = "sonidos.py/curar.mp3"

    try:
        pygame.mixer.Sound(sonido_curacion).play()
    except:
        pass  # Si el sonido no existe, ignora

    for _ in range(30):
        pantalla.blit(fondo, (0, 0))

        if jugador and jugador.vida > 0:
            jugador.dibujar()
        if aliado and aliado.vida > 0:
            aliado.dibujar()
        if enemigo and enemigo.vida > 0:
            enemigo.dibujar()

        pantalla.blit(texto, (x, y - desplazamiento))
        desplazamiento += 2

        pygame.display.flip()
        reloj.tick(60)
#----------------------------ANIMACION DE CURACION------------------------------------#

