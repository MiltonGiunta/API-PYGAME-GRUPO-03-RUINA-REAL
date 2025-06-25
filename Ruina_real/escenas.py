import pygame
import sys
from config import pantalla, fuente, TAMAÑO_FUENTE_CREDITOS, ANCHO, ALTO, NEGRO, ROJO, BLANCO



#----------------------------------CINEMATICAS----------------------------------------#
def play_cinematic(image_files, audio_files):
    # Aseguramos que haya la misma cantidad de imágenes que de audios
    if len(image_files) != len(audio_files):
        print("Error: La cantidad de imágenes y audios no coincide para la cinemática.")
        return
    pygame.mixer.music.set_volume(0.5)

    # Iteramos sobre los índices para acceder a la imagen y su audio correspondiente
    for i in range(len(image_files)):
        # Cargar y escalar la imagen
        try:
            img = pygame.transform.scale(pygame.image.load(image_files[i]), (ANCHO, ALTO))
        except pygame.error as e:
            print(f"Error al cargar la imagen {image_files[i]}: {e}")
            continue # Pasa a la siguiente iteración si hay un error con la imagen

        # Cargar y reproducir el audio
        current_audio_path = audio_files[i]
        try:
            pygame.mixer.music.load(current_audio_path) # Usamos pygame.mixer.music para archivos largos
            pygame.mixer.music.play() # Reproduce el audio una vez
        except pygame.error as e:
            print(f"Error al cargar o reproducir el audio {current_audio_path}: {e}")
            # Si hay un error con el audio, la cinemática puede continuar sin sonido
            
        # Limpiar la pantalla antes de dibujar la nueva imagen y texto
        pantalla.fill(NEGRO) # O el color de fondo que prefieras

        # Dibujar la imagen
        pantalla.blit(img, (0, 0))

        # Renderizar y posicionar el texto
        texto = fuente.render("Presiona A para continuar", True, (ROJO))
        texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO - 30)) # Ubicación más centrada y abajo
        pantalla.blit(texto, texto_rect)
        pygame.display.flip() # Actualiza la pantalla para mostrar la imagen y el texto

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    esperando = False
                    pygame.mixer.music.stop() # Detiene el audio actual antes de pasar al siguiente
            
            # Un pequeño delay para no consumir CPU innecesariamente en el bucle de eventos
            pygame.time.Clock().tick(60) # Limita a 60 frames por segundo el bucle de espera

#----------------------------------CINEMATICAS----------------------------------------#


#------------------------------------CREDITOS-----------------------------------------#    
def mostrar_creditos(pantalla):
    fuente = pygame.font.SysFont("GODOFWAR", TAMAÑO_FUENTE_CREDITOS)
    pygame.mixer.music.load("sonidos.py/Música medieval 4.mp3")                                 # sonido 
    pygame.mixer.music.set_volume(0.3)                                                          # controla el volumen del sonido
    pygame.mixer.music.play()         

    creditos = [
        " DESARROLLADO POR ", " Giunta Milton ", " Popp Lautaro Roman ", " Lopez Juan Jose ",
        " Kuo Daniel Matias ", " Quiroga Nicolas Juan Benjamin ", " Salibi Maximiliano ",
        "", " DISENIADO POR ","(la tipografia no tiene enie)", " Meta, ChatGPT, Gemini, Grok",
        "", " MUSICA", " Super Pirateada", "",
        " HISTORIA", " ChatGPT, BotTelegram", "", " INSPIRADOS EN", " Shakes and Fidget ", "",
        " PROFESORES", " Volker Mariano Leonardo ", " Hirschfeldt Dario ", "",
        " FRASE DEL DIA", " Un gran poder conlleva", " una gran responsabilidad", " TIO BEN ", "",
        " Gracias por jugar "
    ]

    superficies_creditos = [fuente.render(linea, True, BLANCO) for linea in creditos]
    posiciones_y = [pantalla.get_height() + i * 50 for i in range(len(creditos))]
    velocidad = 5
    reloj = pygame.time.Clock()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        victoria = pygame.transform.scale(pygame.image.load("cinematicas/imagen_final_opacidad.png"), (ANCHO, ALTO))
        pantalla.blit(victoria, (0 ,0))   

        for i, superficie in enumerate(superficies_creditos):
            y = posiciones_y[i]
            pantalla.blit(superficie, (pantalla.get_width() // 2 - superficie.get_width() // 2, y))
            posiciones_y[i] -= velocidad

        if posiciones_y[-1] < -50:
            corriendo = False
            pygame.exit()
            sys.exit()

        pygame.display.flip()
        reloj.tick(60)
#------------------------------------CREDITOS-----------------------------------------#
