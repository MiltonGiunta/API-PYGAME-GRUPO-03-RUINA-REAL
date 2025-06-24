import pygame
import sys
from config import pantalla, fuente, reloj, ANCHO, ALTO, ROJO, BLANCO, VERDE


#--------------------------INTRO Y PARPADEO DE TEXTO----------------------------------#
def pantalla_inicio():
 imagen_intro = pygame.transform.scale(pygame.image.load("assets.py/intro.jpg"), (ANCHO, ALTO))
 texto = fuente.render("Presiona cualquier tecla para comenzar", True, (ROJO))               # reenderiza el texto, y pinta el color marcado
 texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 1.1))                               # posiciona y dividiendo el ancho y el alto de la pantalla
 pygame.mixer.music.load("sonidos.py/Música de ambiente 6.mp3")                              # sonido 
 pygame.mixer.music.set_volume(0.3)                                                          # controla el volumen del sonido
 pygame.mixer.music.play()                                                                   # reproduce el sonido
 mostrar = True                                                                              # muestra el texto siempre
 intervalo = 250                                                                             # milisegundos 
 ultimo_cambio = pygame.time.get_ticks()
 corriendo = True                                                                            # inicia el bucle de cerrar cuando se toque una tecla
 while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN:                      # cuando se precione cualquier tecla, salta a la siguiente pantalla
            corriendo = False

    ahora = pygame.time.get_ticks()                                                          # inicia el bucle del texto parpadenate
    if ahora - ultimo_cambio >= intervalo:                                                  
        mostrar = not mostrar
        ultimo_cambio = ahora


    pantalla.blit(imagen_intro, (0, 0))                                                      # muestra la pantalla de inicio con el texto parpadeando
    if mostrar:
        pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    reloj.tick(60)
#--------------------------INTRO Y PARPADEO DE TEXTO----------------------------------#


#--------------------------------MENU DE COMBATE--------------------------------------#
def mostrar_menu_combate(pantalla, fuente):
    pantalla.blit(fuente.render("A - Atacar", True, BLANCO),(50, 700))
    pantalla.blit(fuente.render("C - Curarse", True, BLANCO),(50, 740))
    pygame.display.flip()
#--------------------------------MENU DE COMBATE--------------------------------------#


#------------------------------PANTALLA DERROTA---------------------------------------#
def mostrar_pantalla_game_over(pantalla, fuente):
    derrota = pygame.transform.scale(pygame.image.load("cinematicas/Derrota_opacidad.png"), (ANCHO, ALTO))
    pantalla.blit(derrota, (0, 0))   
    texto = fuente.render("¡Perdiste! Queres volver a jugar?", True, (BLANCO))
    si_texto = fuente.render("S - Si", True, (VERDE))
    no_texto = fuente.render("N - No", True, (ROJO))

    pantalla.blit(texto, (100, 200))
    pantalla.blit(si_texto, (100, 300))
    pantalla.blit(no_texto, (100, 350))
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    return True  
                elif evento.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
#------------------------------PANTALLA DERROTA---------------------------------------#


#-----------------------------MUESTRA VITORIA/DERROTA---------------------------------#
# muestra una pantalla despues del combate
def mostrar_cartel_victoria():                                                               
    victoria = pygame.transform.scale(pygame.image.load("cinematicas/Victoria.png"), (ANCHO, ALTO))
    pantalla.blit(victoria, (0 ,0))                                                                  
    pygame.display.flip()
    pygame.time.wait(2000) # despues de 2segundos se sale automaticamente esta pantalla                                                                 

def mostrar_cartel_derrota():                                                               
    derrota = pygame.transform.scale(pygame.image.load("cinematicas/Derrota.png"), (ANCHO, ALTO))
    pantalla.blit(derrota, (0, 0))                                                                  
    pygame.display.flip()
    pygame.time.wait(2000)
#-----------------------------MUESTRA VITORIA/DERROTA---------------------------------#


#---------------------------------MENU COMPAÑERO--------------------------------------#
def mostrar_menu():                                                                         # menu de seleccion de aliado
    fondo2 = pygame.transform.scale(pygame.image.load("assets.py/fondo2.jpeg"), (ANCHO, ALTO))
    pantalla.blit(fondo2, (0, 0))
    pygame.mixer.music.load("narrativa.py/Narracion 10.mp3")                                # Usamos pygame.mixer.music para archivos largos
    pygame.mixer.music.play()                                                               # Reproduce el audio una vez    
    texto = fuente.render("Salvar al Orco (S/N)", True, (BLANCO))
    pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 1.1)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:                                                # nos da la opcion de seleccionar si queremos salvar o no al personaje
                if event.key == pygame.K_s:                                                 # en caso de salvarlo, se hace nuestro aliado
                    return True                  
                elif event.key == pygame.K_n:                                               # en caso de no salvarlo peleamos solos
                    return False
#---------------------------------MENU COMPAÑERO--------------------------------------#


#----------------------------MUESTRA INICIO DE COMBATE--------------------------------#
def mostrar_cartel_inicio():                                                                # muestra el inicio del combate
    combate = pygame.transform.scale(pygame.image.load("cinematicas/Combate.jpeg"), (ANCHO, ALTO))                                            
    texto = fuente.render("Preparate para el combate", True, (BLANCO))
    pantalla.blit(combate, (0 ,0))       
    pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 1.1)))
    pygame.display.flip()
    pygame.time.wait(2000)
#----------------------------MUESTRA INICIO DE COMBATE--------------------------------#
