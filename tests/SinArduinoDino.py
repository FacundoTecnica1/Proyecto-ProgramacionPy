import pygame
import random
import sys
import serial 

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 400
FPS = 60

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dinosaurio con 2 imágenes")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
fuente = pygame.font.SysFont("Arial", 28)

# ==============================
# CARGA DE IMÁGENES
# ==============================
try:
    dino_img = pygame.image.load("img/dino.png").convert_alpha()
    cactus_img = pygame.image.load("img/cactus1.png").convert_alpha()
except pygame.error as e:
    print("Error al cargar imágenes:", e)
    sys.exit()

# Escalar imágenes
dino_img = pygame.transform.scale(dino_img, (60, 60))
cactus_img = pygame.transform.scale(cactus_img, (40, 60))

# ==============================
# VARIABLES DEL JUEGO
# ==============================
# Dinosaurio
dino_x = 50
dino_y = ALTO - 60 - dino_img.get_height()
dino_vel_y = 0
gravedad = 1.2
en_suelo = True

# Obstáculos
obstaculos = []
velocidad_obstaculos = 6
tiempo_ultimo_obstaculo = 0
tiempo_entre_obstaculos = 1500  # ms

# Puntuación
puntaje = 0
record = 0
juego_activo = True

# Reloj
clock = pygame.time.Clock()

# ==============================
# FUNCIONES
# ==============================
def mostrar_texto(texto, x, y, color=NEGRO, tamaño=28):
    fuente_local = pygame.font.SysFont("Arial", tamaño)
    render = fuente_local.render(texto, True, color)
    ventana.blit(render, (x, y))

def reiniciar_juego():
    global dino_y, dino_vel_y, en_suelo, obstaculos, puntaje, juego_activo
    dino_y = ALTO - 60 - dino_img.get_height()
    dino_vel_y = 0
    en_suelo = True
    obstaculos.clear()
    puntaje = 0
    juego_activo = True

def crear_obstaculo():
    rect = cactus_img.get_rect()
    rect.x = ANCHO + random.randint(0, 100)
    rect.y = ALTO - 60 - rect.height
    return rect

# ==============================
# BUCLE PRINCIPAL
# ==============================
while True:
    dt = clock.tick(FPS)
    ventana.fill(BLANCO)

    # --------------------------
    # EVENTOS
    # --------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if juego_activo:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and en_suelo:
                    dino_vel_y = -18
                    en_suelo = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reiniciar_juego()

    if juego_activo:
        # --------------------------
        # MOVIMIENTO DEL DINOSAURIO
        # --------------------------
        dino_vel_y += gravedad
        dino_y += dino_vel_y

        if dino_y >= ALTO - 60 - dino_img.get_height():
            dino_y = ALTO - 60 - dino_img.get_height()
            en_suelo = True

        # --------------------------
        # GENERAR OBSTÁCULOS
        # --------------------------
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_obstaculo > tiempo_entre_obstaculos:
            obstaculos.append(crear_obstaculo())
            tiempo_ultimo_obstaculo = tiempo_actual

        # Mover y dibujar obstáculos
        for obstaculo in obstaculos:
            obstaculo.x -= velocidad_obstaculos
            ventana.blit(cactus_img, obstaculo)

        # Eliminar obstáculos que salen
        obstaculos = [o for o in obstaculos if o.x + o.width > 0]

        # --------------------------
        # DETECCIÓN DE COLISIONES
        # --------------------------
        dino_rect = pygame.Rect(dino_x, dino_y, dino_img.get_width(), dino_img.get_height())
        for obstaculo in obstaculos:
            if dino_rect.colliderect(obstaculo):
                juego_activo = False
                if puntaje > record:
                    record = int(puntaje)

        # --------------------------
        # ACTUALIZAR PUNTUACIÓN
        # --------------------------
        puntaje += 0.1

        # --------------------------
        # DIBUJAR DINOSAURIO
        # --------------------------
        ventana.blit(dino_img, (dino_x, dino_y))

        # --------------------------
        # HUD
        # --------------------------
        mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10)
        mostrar_texto(f"Record: {record}", ANCHO - 150, 10)

    else:
        # Pantalla de Game Over
        mostrar_texto("GAME OVER", ANCHO // 2 - 80, ALTO // 2 - 30, NEGRO, 36)
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2 - 160, ALTO // 2 + 20)

    pygame.display.flip()