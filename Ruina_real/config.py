# RESOLUCION #
ANCHO, ALTO = 800, 800  # ancho y alto de la ventana

#colores
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)
GRIS = (75, 75, 75)

#tamaño de fuentes
TAMAÑO_FUENTE = 30
TAMAÑO_FUENTE_CREDITOS = 40

# inicia pygame.
pygame.init()       

# inicia los sonidos dentro de pygame
pygame.mixer.init()  

# crea la ventana con el ancho y alto asigando y le da un titulo a la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))                                            
pygame.display.set_caption("Ruina Real")

# fuente y tamaño de la fuente
fuente = pygame.font.SysFont("GODOFWAR", TAMAÑO_FUENTE)

# crea un reloj q controla los fps
reloj = pygame.time.Clock()
