import pygame
import sys
import time
import random
from config import pantalla, reloj, ANCHO, ALTO, fuente,TAMAÑO_FUENTE_CREDITOS, VERDE, ROJO
from utils import dibujar_mensaje, esperar_eleccion_jugador, animacion_curacion, mostrar_mensaje_superior , esquiva
from menu import pantalla_inicio, mostrar_pantalla_game_over, mostrar_menu, mostrar_cartel_inicio, mostrar_cartel_derrota, mostrar_menu_combate, mostrar_cartel_victoria
from escenas import play_cinematic, mostrar_creditos

#----------------------------CARTEL DE DERROTA ALIADO---------------------------------#
def mostrar_mensaje_eliminacion(texto, superficie, fuente, jugador, aliado, enemigo, duracion=4): # LLama a un cartel que inidica la muerte del personaje
    mensaje = fuente.render(texto, True, (ROJO))
    mensaje.set_alpha(0)  # Comienza totalmente transparente
    rect = mensaje.get_rect(center=(ANCHO // 2, ALTO // 4))

    tiempo_inicio = time.time()
    alpha = 0

    while time.time() - tiempo_inicio < duracion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        superficie.blit(fondo_actual, (0, 0))
        jugador.dibujar()
        if aliado and aliado.vida > 0:
            aliado.dibujar()
        enemigo.dibujar()
        dibujar_mensaje()

        # Fade in del mensaje
        if alpha < 255:
            alpha += 10
            mensaje.set_alpha(min(alpha, 255))

        superficie.blit(mensaje, rect)
        pygame.display.flip()
        reloj.tick(60)
#----------------------------CARTEL DE DERROTA ALIADO---------------------------------#
#--------------------------------CLASE PERSONAJES-------------------------------------#
class Personaje:
    def __init__(self, nombre, imagen, posicion, vida_max, poder_normal, curar):
        self.nombre = nombre
        self.imagen_original = imagen
        self.imagen = imagen.copy()
        self.x, self.y = posicion
        self.vida_max = vida_max
        self.vida = vida_max
        self.poder_normal = poder_normal
        self.curar = curar
#--------------------------------CLASE PERSONAJES-------------------------------------#
#------------------------------PROBABILIDAD CURARSE-----------------------------------#
    def sanar(self, cantidad,):
       if self.vida <= 0:
        return
       self.vida = min(self.vida + cantidad, self.vida_max)   
       mostrar_mensaje_superior(f"{self.nombre} se cura {cantidad} puntos. Vida actual: {self.vida}")
#------------------------------PROBABILIDAD CURARSE-----------------------------------#
#----------------------------DIBUJA LA BARRA DE VIDA----------------------------------#
    def dibujar(self):
        ancho = self.imagen.get_width()
        alto = self.imagen.get_height()
        pantalla.blit(self.imagen, (self.x - ancho // 2, self.y - alto // 2))
        proporcion = self.vida / self.vida_max
        pygame.draw.rect(pantalla, (ROJO), (self.x - 100, self.y - 115, ancho, 8))
        pygame.draw.rect(pantalla, (VERDE), (self.x - 100, self.y - 115, int(ancho * proporcion), 8))
#----------------------------DIBUJA LA BARRA DE VIDA----------------------------------#
#--------------------------------ESQUIVE Y DAÑO---------------------------------------#
    def atacar(self, objetivo):
        self.animar_ataque(objetivo)
        if esquiva(15):
          objetivo.vida -= self.poder_normal
          mostrar_mensaje_superior(f"{self.nombre} ataca a {objetivo.nombre} - Vida restante: {objetivo.vida}")
        else:
          mostrar_mensaje_superior(f"{objetivo.nombre} esquivo el ataque de {self.nombre}")

        if objetivo.vida < 0:
            objetivo.vida = 0
#--------------------------------ESQUIVE Y DAÑO---------------------------------------#
#-----------------------------ANIMACION DE COMBATE------------------------------------#
    def animar_ataque(self, objetivo):                                                      # animacion de ataque, que realiza un golpe similar a "HEARSTONE"
        if self.vida <= 0:
         return                                                                             # No hace animación si está muerto
        
        if self.nombre in ["Jugador", "Aliado"]:
            Espada = pygame.mixer.Sound("sonidos.py/Espada.mp3")                            # esta funcion hace que solo pueda escuchar el sonido sobre otro de fondo
            pasos = 22                                                                      # son los movimientos que realiza la animacion en el combate
            dx = (objetivo.x - self.x) // pasos                                             # Aca busca al metodo objetivo y lo sigue restando en la posicion
            dy = (objetivo.y - self.y) // pasos                                             # que se encuentre el objetivo dividiendo los pasos
            for i in range(pasos):                                                          # Aca despues de tocar el objetivo vuelve a su posicion original
                self.x += dx                                                                # respetando el recorrido 
                self.y += dy
                self._refrescar_combate(objetivo)
                Espada.play()
            for i in range(pasos):
                self.x -= dx
                self.y -= dy
                self._refrescar_combate(objetivo)
        else:
            Puno = pygame.mixer.Sound("sonidos.py/Puño.mp3")                                # aca hago lo mismo pero para el enemigo
            pasos = 10
            dx = (objetivo.x - self.x) // pasos
            dy = (objetivo.y - self.y) // pasos
            for i in range(pasos):
                self.x += dx
                self.y += dy
                self._refrescar_combate(objetivo)
                Puno.play()
            for i in range(pasos):
                self.x -= dx
                self.y -= dy
                self._refrescar_combate(objetivo)
#-----------------------------ANIMACION DE COMBATE------------------------------------#
#------------------VISUALIZACION Y ACTUALIZACION DE COMBATE---------------------------#
    def _refrescar_combate(self, objetivo):                                                 # actualizo en tiempo real la imagen entre los personajes y el objetivo
        pantalla.blit(fondo_actual, (0, 0))
        if self.nombre == "Jugador":
            self.dibujar()
            if aliado and aliado.vida > 0:
                aliado.dibujar()
            objetivo.dibujar()
        elif self.nombre == "Aliado":
            jugador.dibujar()
            self.dibujar()
            objetivo.dibujar()
        else:
            jugador.dibujar()
            if aliado and aliado.vida > 0:
                aliado.dibujar()
            self.dibujar()
        pygame.display.flip()
        reloj.tick(60)
#------------------VISUALIZACION Y ACTUALIZACION DE COMBATE---------------------------#


#------------------------------------COMBATE------------------------------------------#
def combate(jugador_, aliado_, enemigo, fondo_personalizado=None):                       # aca hacemos que el combate pueda ocurrir con el jugador, el aliado contra el enemigo y tenemos un fondo personalizado                        
    mostrar_cartel_inicio() 
    global jugador, aliado, fondo_actual
    jugador, aliado = jugador_, aliado_                                                  # el jugador combate con el aliado en el mismo equipo
    turno = 0                                                                            # comienza en turno 0
    tiempo_ultimo_ataque = time.time()
    tiempo_entre_ataques = 1.5                                                           # tiempo que tarda en realizar los ataques los personajes
    aliado_derrotado = False

    if fondo_personalizado:
        fondo = pygame.transform.scale(pygame.image.load(fondo_personalizado), (ANCHO, ALTO))
    else:
        fondo = pygame.transform.scale(pygame.image.load("assets.py/fondo.jpg"), (ANCHO, ALTO))

    fondo_actual = fondo

    pygame.mixer.music.load("sonidos.py/Musica medieval 3.mp3")
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(loops=-1)                                                    # Reproduce en bucle infinito

    while jugador.vida > 0 and enemigo.vida > 0:                                         # empieza el bucle, cuando alguno de los dos tipos de personajes llegue a 0
        for evento in pygame.event.get():                                                # la pantalla se va a cerrar
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.blit(fondo, (0, 0))
        dibujar_mensaje()
        jugador.dibujar()
        if aliado and aliado.vida > 0:
            aliado.dibujar()
        enemigo.dibujar()
                                                                          
        if aliado and aliado.vida <= 0 and not aliado_derrotado:                         # Mostrar mensaje si el aliado muere por primera vez
            aliado_derrotado = True
            mostrar_mensaje_eliminacion(f"¡{aliado.nombre} ha sido noqueado!", pantalla, fuente, jugador, aliado, enemigo)
            muerte = pygame.mixer.Sound("sonidos.py/muerte_aliado.mp3")
            muerte.play()

        if time.time() - tiempo_ultimo_ataque >= tiempo_entre_ataques:                   # llama a la funcion de ataques para realizar el combate
            if turno == 0:
                mostrar_menu_combate(pantalla, fuente)
                eleccion = esperar_eleccion_jugador()
                if eleccion == "atacar":
                    jugador.atacar(enemigo)
                elif eleccion == "curar":
                    jugador.sanar(300)
                    animacion_curacion(jugador, 300, pantalla, fondo, jugador=jugador, aliado=aliado, enemigo=enemigo)

            elif turno == 1 and aliado and aliado.vida > 0:                              # suma un turno si el aliado esta presente
                if aliado.vida < 400 and random.random() < 0.5: 
                    aliado.sanar(200)
                    animacion_curacion(aliado, 200, pantalla, fondo, jugador=jugador, aliado=aliado, enemigo=enemigo)
                else:
                    aliado.atacar(enemigo)

            elif turno == 2:
                if enemigo.vida < enemigo.vida_max * 0.4 and random.random() < 0.5:      # enemigo adquiere la funcion de curar
                    enemigo.sanar(400)
                    animacion_curacion(enemigo, 400, pantalla, fondo, jugador=jugador, aliado=aliado, enemigo=enemigo)
                else:
                    objetivo = jugador if random.randint(0, 1) == 0 or not (aliado and aliado.vida > 0) else aliado
                    if objetivo and objetivo.vida > 0:                                   # el aliado adquiere la funcion de esquivar
                        enemigo.atacar(objetivo)
                                                   
            jugador_vivo = jugador.vida > 0                                              # Actualizar turno: solo cuentan los personajes vivos
            aliado_vivo = aliado and aliado.vida > 0
            enemigo_vivo = enemigo.vida > 0

            siguiente_turno = (turno + 1) % 3
            for _ in range(3):                                                           # hasta que encuentre un turno válido
                if siguiente_turno == 0 and jugador_vivo:
                    turno = 0
                    break
                elif siguiente_turno == 1 and aliado_vivo:
                    turno = 1
                    break
                elif siguiente_turno == 2 and enemigo_vivo:
                    turno = 2
                    break
                siguiente_turno = (siguiente_turno + 1) % 3

            tiempo_ultimo_ataque = time.time()

        pygame.display.flip()
        reloj.tick(60)

    # Fin del combate
    if jugador.vida <= 0:
        pygame.mixer.music.load("sonidos.py/Puño.mp3")
        pygame.mixer.music.play()
        mostrar_cartel_derrota()
        reiniciar = mostrar_pantalla_game_over(pantalla, fuente)
        if reiniciar:
            from main import main
            main()
        else:
            pygame.quit()
            sys.exit()                                                                 # Llama de nuevo a la función principal
    else:
        pygame.mixer.music.load("sonidos.py/Correct.mp3")
        pygame.mixer.music.play()
        mostrar_cartel_victoria()
#------------------------------------COMBATE------------------------------------------#
def main():
    
    pantalla_inicio()
    fuente = pygame.font.SysFont(None, TAMAÑO_FUENTE_CREDITOS)
    #---------------------------CINEMATICAS-----------------------------------#
    cinematic_images = [
        "cinematicas/Jugador.png",
        "cinematicas/Familia.png",
        "cinematicas/Rey.png",
        "cinematicas/cinematic1.jpeg",
        "cinematicas/cinematic2.jpeg",
        "cinematicas/cinematic3.jpeg"
    #---------------------------CINEMATICAS-----------------------------------#
    #---------------------------NARRACIONES-----------------------------------#    
    ]
    cinematic_audio = [
        "narrativa.py/Narracion 1.mp3",
        "narrativa.py/Narracion 2.mp3",
        "narrativa.py/Narracion 3.mp3",
        "narrativa.py/Narracion 4.mp3",
        "narrativa.py/Narracion 5.mp3",
        "narrativa.py/Narracion 6.mp3"
    ]
    #---------------------------NARRACIONES-----------------------------------#
    #------------------------------FONDOS-------------------------------------#
    fondo_bosque = "cinematicas/bosque1.jpeg"
    fondo_castillo = "cinematicas/Castillo - Pasillos.png"
    fondo_casa = "cinematicas/casa.jpg"
    #------------------------------FONDOS-------------------------------------#
    #----------------------------PERSONAJES-----------------------------------#
    imagen_jugador = pygame.transform.scale(pygame.image.load("assets.py/jugador.png"), (200, 200))
    imagen_aliado = pygame.transform.scale(pygame.image.load("assets.py/orco-marco.png"), (200, 200))
    imagen_lobos = pygame.transform.scale(pygame.image.load("assets.py/marco-lobos.png"), (200, 200))
    imagen_paladin = pygame.transform.scale(pygame.image.load("assets.py/paladin.png"), (200, 200))
    imagen_bandido = pygame.transform.scale(pygame.image.load("assets.py/marco-bandido.png"), (200, 200))
    imagen_aldeanos = pygame.transform.scale(pygame.image.load("assets.py/marco_aldeanos.png"), (200, 200))
    #----------------------------PERSONAJES-----------------------------------#
    play_cinematic(cinematic_images, cinematic_audio)
    #----------POSICION Y ESTADISITICAS DE LOS PERSONAJES---------------------#
    jugador_ = Personaje("Jugador", imagen_jugador, (560, 400), 2500, 750, 450)
    aliado_ = Personaje("Aliado", imagen_aliado, (560, 600), 1000, 500, 250)
    lobos = Personaje("Lobo", imagen_lobos, (240, 400), 1500, 300, 200)
    paladin = Personaje("Paladin", imagen_paladin, (240, 400), 4000, 600, 750)
    bandido = Personaje("Bandido", imagen_bandido, (240, 400), 2250, 400, 500)
    aldeanos = Personaje("Aldeanos", imagen_aldeanos, (240, 400), 3000, 550, 600)
    #----------POSICION Y ESTADISITICAS DE LOS PERSONAJES---------------------#
    combate(jugador_, None, lobos)                                                    # comienza el primer combate 

    play_cinematic(["cinematicas/bosque1.jpeg", "cinematicas/bosque2.png"], ["narrativa.py/Narracion 7 A.mp3", "narrativa.py/Narracion 7 B.mp3"])
    combate(jugador_, None, bandido, fondo_bosque)                                    # comienza el segundo combate
   
    play_cinematic(["cinematicas/cinematic4.jpeg", "cinematicas/cinematic5.jpeg"], ["narrativa.py/Narracion 8.mp3", "narrativa.py/Narracion 9.mp3"])
    decision = mostrar_menu()

    jugador_.vida = jugador_.vida_max
    aliado_.vida = aliado_.vida_max
    combate(jugador_, aliado_ if decision else None, aldeanos, fondo_casa)            # comienza el tercer combate 
    

    play_cinematic(["cinematicas/cinematic6.jpeg", "cinematicas/cinematic7.jpeg", "cinematicas/cinematic8.jpeg"], ["narrativa.py/Narracion 11.mp3", "narrativa.py/Narracion 12.mp3", "narrativa.py/Narracion 13.mp3"])
    jugador_.vida = jugador_.vida_max
    aliado_.vida = aliado_.vida_max
    combate(jugador_, aliado_ if decision else None, paladin, fondo_castillo)        # comienza el cuarto combate
    
    play_cinematic(["cinematicas/Castillo - Pasillos.png", "cinematicas/Castillo - Sala del clérigo.png"], ["narrativa.py/Narracion 14.mp3", "narrativa.py/Narracion 15.mp3"])    
    mostrar_creditos(pantalla)

if __name__ == "__main__":
    main()
