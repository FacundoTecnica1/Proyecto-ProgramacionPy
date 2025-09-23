import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo
from utils import mostrar_texto

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 450
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Corredor Lunar")

# Rutas de archivos
RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_ESPACIO_FONDO = (30, 30, 35)

# ==============================
# CARGA DE IMÁGENES
# ==============================
try:
    imagenes = {
        'perro_corriendo': [
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run3.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run4.png")).convert_alpha()
        ],
        # Add the jump and air images
        'perro_salto': pygame.image.load(os.path.join(RUTA_BASE, "perro_jump.png")).convert_alpha(),
        'perro_aire': pygame.image.load(os.path.join(RUTA_BASE, "perro_air.png")).convert_alpha(),
        'cactus': [
            pygame.image.load(os.path.join(RUTA_BASE, "cactus1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "cactus2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "cactus3.png")).convert_alpha()
        ],
        'fondo_completo': pygame.image.load(os.path.join(RUTA_BASE, "fondo.png")).convert(),
        'game_over': pygame.image.load(os.path.join(RUTA_BASE, "game_over.png")).convert_alpha(),
        'luna': pygame.image.load(os.path.join(RUTA_BASE, "luna.png")).convert_alpha()
    }
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    pygame.quit()
    sys.exit()

imagenes['fondo_completo'] = pygame.transform.scale(imagenes['fondo_completo'], (ANCHO, ALTO))

# ==============================
# VARIABLES DEL JUEGO
# ==============================
ALTURA_SUELO = 80

perro_corriendo_imgs = [pygame.transform.scale(img, (80, 80)) for img in imagenes['perro_corriendo']]
# Scale the new images
perro_salto_img = pygame.transform.scale(imagenes['perro_salto'], (80, 80))
perro_aire_img = pygame.transform.scale(imagenes['perro_aire'], (80, 80))
cactus_imgs = [pygame.transform.scale(img, (120, 150)) for img in imagenes['cactus']]

# Pass all the necessary images to the Perro class
perro = Perro(perro_corriendo_imgs, perro_salto_img, perro_aire_img, ANCHO, ALTO, ALTURA_SUELO)
fondo_completo = Fondo(imagenes['fondo_completo'], 0.5) 
obstaculos = pygame.sprite.Group()

puntaje = 0
record = 0
juego_activo = True
velocidad_juego = 6
tiempo_ultimo_obstaculo = pygame.time.get_ticks()

reloj = pygame.time.Clock()

# ==============================
# BUCLE PRINCIPAL
# ==============================
while True:
    dt = reloj.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if juego_activo:
            perro.manejar_salto(event)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            perro.reiniciar(ALTO, ALTURA_SUELO)
            obstaculos.empty()
            puntaje = 0
            juego_activo = True
            velocidad_juego = 6
            tiempo_ultimo_obstaculo = pygame.time.get_ticks()

    if juego_activo:
        fondo_completo.actualizar(velocidad_juego)
        perro.actualizar(dt)
        obstaculos.update()

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_obstaculo > 1500:
            if random.random() < 0.7:
                obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
                tiempo_ultimo_obstaculo = tiempo_actual

        if pygame.sprite.spritecollide(perro, obstaculos, False, pygame.sprite.collide_mask):
            juego_activo = False
            if puntaje > record:
                record = int(puntaje)

        puntaje += 0.1
        if puntaje % 100 == 0 and velocidad_juego < 15:
            velocidad_juego += 0.5
            
    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo_completo.dibujar(VENTANA)
    perro.dibujar(VENTANA)
    obstaculos.draw(VENTANA)

    mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
    mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)

    if not juego_activo:
        game_over_rect = imagenes['game_over'].get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
        VENTANA.blit(imagenes['game_over'], game_over_rect)
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 50, BLANCO, VENTANA, centrado=True)
        mostrar_texto(f"Tu puntuación: {int(puntaje)}", ANCHO // 2, ALTO // 2 + 80, BLANCO, VENTANA, centrado=True)
        mostrar_texto(f"Record: {record}", ANCHO // 2, ALTO // 2 + 100, BLANCO, VENTANA, centrado=True)

    pygame.display.flip()