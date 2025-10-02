import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo, Ave
from utils import mostrar_texto
from menu import Menu

pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN DE LA VENTANA Y CONSTANTES ---
ANCHO = 800
ALTO = 450
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino Perro")

# --- RUTA CORRECTA A LAS IMÁGENES ---
RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

# --- COLORES ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_ESPACIO_FONDO = (30, 30, 35)

# --- CARGA Y PROCESAMIENTO DE IMÁGENES ---
try:
    imagenes = {
        'perro_corriendo': [
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run3.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "perro_run4.png")).convert_alpha()
        ],
        'perro_salto': pygame.image.load(os.path.join(RUTA_BASE, "perro_jump.png")).convert_alpha(),
        'perro_aire': pygame.image.load(os.path.join(RUTA_BASE, "perro_air.png")).convert_alpha(),
        'cactus': [
            pygame.image.load(os.path.join(RUTA_BASE, "cactus1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "cactus2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "cactus3.png")).convert_alpha()
        ],
        'fondo_completo': pygame.image.load(os.path.join(RUTA_BASE, "fondo.png")).convert(),
        'game_over': pygame.image.load(os.path.join(RUTA_BASE, "game_over.png")).convert_alpha(),
        'luna': pygame.image.load(os.path.join(RUTA_BASE, "luna.png")).convert_alpha(),
        'ave': [
            pygame.image.load(os.path.join(RUTA_BASE, "ave1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "ave2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "ave3.png")).convert_alpha()
        ]
    }
except pygame.error as e:
    print(f"Error al cargar imágenes desde la ruta '{RUTA_BASE}': {e}")
    pygame.quit()
    sys.exit()

imagenes['fondo_completo'] = pygame.transform.scale(imagenes['fondo_completo'], (ANCHO, ALTO))
ALTURA_SUELO = 30

perro_corriendo_imgs = [pygame.transform.scale(img, (150, 150)) for img in imagenes['perro_corriendo']]
perro_salto_img = pygame.transform.scale(imagenes['perro_salto'], (150, 150))
perro_aire_img = pygame.transform.scale(imagenes['perro_aire'], (150, 150))
cactus_imgs = [pygame.transform.scale(img, (110, 140)) for img in imagenes['cactus']]
ANCHO_CACTUS_PEQ = int(110 * 0.75)
ALTO_CACTUS_PEQ = int(140 * 0.75)
cactus_pequeno_imgs = [pygame.transform.scale(img, (ANCHO_CACTUS_PEQ, ALTO_CACTUS_PEQ)) for img in imagenes['cactus']]
luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))
ave_imgs = [pygame.transform.scale(img, (100, 80)) for img in imagenes['ave']]

# --- INICIALIZACIÓN DE OBJETOS Y VARIABLES DEL JUEGO ---
perro = Perro(perro_corriendo_imgs, perro_salto_img, perro_aire_img, ANCHO, ALTO, ALTURA_SUELO)
fondo_completo = Fondo(imagenes['fondo_completo'], 0.5)
obstaculos = pygame.sprite.Group()
aves = pygame.sprite.Group()

puntaje = 0
record = 0
juego_activo = False
velocidad_juego = 5.5

tiempo_ultimo_obstaculo = pygame.time.get_ticks()
intervalo_proximo_cactus = random.randint(1000, 3000)
tiempo_ultima_ave = pygame.time.get_ticks()
intervalo_proxima_ave = random.randint(4000, 8000)

CHANCE_DOBLE_CACTUS = 0.5
SEPARACION_DOBLE_CACTUS_MIN = 60
SEPARACION_DOBLE_CACTUS_MAX = 90
CHANCE_SEGUNDO_CACTUS_PEQUENO = 0.9

reloj = pygame.time.Clock()

# --- MENÚ INICIAL ---
menu = Menu(VENTANA, ANCHO, ALTO, record)
accion = menu.mostrar()
if accion == "jugar":
    juego_activo = True
else:
    pygame.quit()
    sys.exit()

# --- BUCLE PRINCIPAL DEL JUEGO ---
while True:
    dt = reloj.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if juego_activo:
            perro.manejar_salto(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                perro.reiniciar(ALTO, ALTURA_SUELO)
                obstaculos.empty()
                aves.empty()
                puntaje = 0
                juego_activo = True
                velocidad_juego = 5.5
                tiempo_ultimo_obstaculo = pygame.time.get_ticks()
                intervalo_proximo_cactus = random.randint(1000, 3000)
                tiempo_ultima_ave = pygame.time.get_ticks()
                intervalo_proxima_ave = random.randint(4000, 8000)
            elif event.key == pygame.K_ESCAPE:
                menu.record_actual = record
                accion = menu.mostrar()
                if accion != "jugar":
                    pygame.quit()
                    sys.exit()

    if juego_activo:
        fondo_completo.actualizar(velocidad_juego)
        perro.actualizar(dt)
        obstaculos.update()
        aves.update()

        tiempo_actual = pygame.time.get_ticks()

        # Lógica para generar aves aleatorias
        if tiempo_actual - tiempo_ultima_ave > intervalo_proxima_ave:
            aves.add(Ave(ave_imgs, ANCHO, ALTO, velocidad_juego))
            tiempo_ultima_ave = tiempo_actual
            intervalo_proxima_ave = random.randint(4000, 8000)
            tiempo_ultimo_obstaculo = tiempo_actual

        # Lógica para generar cactus aleatorios
        # Usamos 'elif' para asegurarnos de que no se genere un cactus y un pájaro en el mismo fotograma.
        elif tiempo_actual - tiempo_ultimo_obstaculo > intervalo_proximo_cactus:
            obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
            if random.random() < CHANCE_DOBLE_CACTUS:
                if random.random() < CHANCE_SEGUNDO_CACTUS_PEQUENO:
                    img_segundo_cactus = cactus_pequeno_imgs
                    separacion = random.randint(SEPARACION_DOBLE_CACTUS_MIN, SEPARACION_DOBLE_CACTUS_MAX)
                else:
                    img_segundo_cactus = cactus_imgs
                    separacion = random.randint(SEPARACION_DOBLE_CACTUS_MIN + 20, SEPARACION_DOBLE_CACTUS_MAX + 40)
                obstaculos.add(Obstaculo(img_segundo_cactus, ANCHO + separacion, ALTO, ALTURA_SUELO, velocidad_juego))

            tiempo_ultimo_obstaculo = tiempo_actual
            intervalo_proximo_cactus = random.randint(1000, 3000)
            tiempo_ultima_ave = tiempo_actual

        # Comprobar colisiones
        colision_cactus = pygame.sprite.spritecollide(perro, obstaculos, False, pygame.sprite.collide_mask)
        colision_ave = pygame.sprite.spritecollide(perro, aves, False, pygame.sprite.collide_mask)
        if colision_cactus or colision_ave:
            juego_activo = False
            if puntaje > record:
                record = int(puntaje)

        # Actualizar puntaje y velocidad
        puntaje += 0.1
        if int(puntaje) > 0 and int(puntaje) % 100 == 0:
            if velocidad_juego < 15:
                velocidad_juego += 0.5

    # --- DIBUJADO EN PANTALLA ---
    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo_completo.dibujar(VENTANA)
    obstaculos.draw(VENTANA)
    aves.draw(VENTANA)
    perro.dibujar(VENTANA)
    luna_rect = luna_img.get_rect(topright=(ANCHO - 20, 20))
    VENTANA.blit(luna_img, luna_rect)

    mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
    mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)

    if not juego_activo:
        game_over_rect = imagenes['game_over'].get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
        VENTANA.blit(imagenes['game_over'], game_over_rect)
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 90, BLANCO, VENTANA, centrado=True)
        mostrar_texto("Presiona ESC para volver al menú", ANCHO // 2, ALTO // 2 + 140, BLANCO, VENTANA, centrado=True)

    pygame.display.flip()