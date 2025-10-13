import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo, Ave
from seleccion_personaje import SeleccionPersonaje
from utils import mostrar_texto
from menu import Menu

pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 800, 700
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino Perro 🐶 / 🐱")

RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

BLANCO = (255, 255, 255)
COLOR_ESPACIO_FONDO = (30, 30, 35)
ALTURA_SUELO = 30

# --- CARGA DE IMÁGENES ---
def cargar_imagen(nombre):
    return pygame.image.load(os.path.join(RUTA_BASE, nombre)).convert_alpha()

imagenes = {
    "perro_run": [cargar_imagen(f"perro_run{i}.png") for i in range(1, 5)],
    "perro_jump": cargar_imagen("perro_jump.png"),
    "perro_air": cargar_imagen("perro_air.png"),
    "gato_run": [cargar_imagen(f"gato_run{i}.png") for i in range(1, 5)],
    "gato_jump": cargar_imagen("gato_jump.png"),
    "gato_air": cargar_imagen("gato_air.png"),
    "cactus": [cargar_imagen(f"cactus{i}.png") for i in range(1, 4)],
    "ave": [cargar_imagen(f"ave{i}.png") for i in range(1, 4)],
    "fondo": pygame.image.load(os.path.join(RUTA_BASE, "fondo.png")).convert(),
    "luna": cargar_imagen("luna.png"),
    "game_over": cargar_imagen("game_over.png"),
}

imagenes["fondo"] = pygame.transform.scale(imagenes["fondo"], (ANCHO, ALTO))
luna_img = pygame.transform.scale(imagenes["luna"], (75, 75))

# --- ESCALAS ---
def escalar_lista(lista, w, h):
    return [pygame.transform.scale(img, (w, h)) for img in lista]

perro_run = escalar_lista(imagenes["perro_run"], 150, 150)
gato_run = escalar_lista(imagenes["gato_run"], 150, 150)
perro_jump = pygame.transform.scale(imagenes["perro_jump"], (150, 150))
perro_air = pygame.transform.scale(imagenes["perro_air"], (150, 150))
gato_jump = pygame.transform.scale(imagenes["gato_jump"], (150, 150))
gato_air = pygame.transform.scale(imagenes["gato_air"], (150, 150))
cactus_imgs = escalar_lista(imagenes["cactus"], 110, 140)
cactus_small = escalar_lista(imagenes["cactus"], 82, 105)
ave_imgs = escalar_lista(imagenes["ave"], 100, 80)

# --- MENU PRINCIPAL ---
menu = Menu(VENTANA, ANCHO, ALTO, 0)
if menu.mostrar() != "jugar":
    pygame.quit()
    sys.exit()

# --- SELECCIÓN DE PERSONAJE ---
selector = SeleccionPersonaje(VENTANA, ANCHO, ALTO)
personaje = selector.mostrar()  # devuelve "perro" o "gato"

# --- CREAR JUGADOR ---
if personaje == "gato":
    jugador = Perro(gato_run, gato_jump, gato_air, ANCHO, ALTO, ALTURA_SUELO)
else:
    jugador = Perro(perro_run, perro_jump, perro_air, ANCHO, ALTO, ALTURA_SUELO)

fondo = Fondo(imagenes["fondo"], 0.5)
obstaculos = pygame.sprite.Group()
aves = pygame.sprite.Group()

# --- VARIABLES ---
puntaje = 0
record = 0
juego_activo = True
velocidad_juego = 5.5
reloj = pygame.time.Clock()

tiempo_ultimo_obstaculo = pygame.time.get_ticks()
intervalo_cactus = random.randint(1000, 3000)
tiempo_ultima_ave = pygame.time.get_ticks()
intervalo_ave = random.randint(4000, 8000)

CHANCE_DOBLE_CACTUS = 0.5
CHANCE_SEGUNDO_CACTUS_PEQUENO = 0.9
SEPARACION_MIN = 60
SEPARACION_MAX = 100

# --- LOOP PRINCIPAL ---
while True:
    dt = reloj.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if juego_activo:
            jugador.manejar_salto(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.reiniciar(ALTO, ALTURA_SUELO)
                obstaculos.empty()
                aves.empty()
                puntaje = 0
                velocidad_juego = 5.5
                juego_activo = True
                tiempo_ultimo_obstaculo = pygame.time.get_ticks()
                tiempo_ultima_ave = pygame.time.get_ticks()
            elif event.key == pygame.K_ESCAPE:
                menu.record_actual = record
                if menu.mostrar() != "jugar":
                    pygame.quit()
                    sys.exit()

    if juego_activo:
        fondo.actualizar(velocidad_juego)
        jugador.actualizar(dt)
        obstaculos.update()
        aves.update()

        tiempo_actual = pygame.time.get_ticks()

        # --- AVE ---
        if tiempo_actual - tiempo_ultima_ave > intervalo_ave:
            aves.add(Ave(ave_imgs, ANCHO, ALTO, velocidad_juego))
            tiempo_ultima_ave = tiempo_actual
            intervalo_ave = random.randint(4000, 8000)

        # --- CACTUS ---
        if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_cactus:
            obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
            if random.random() < CHANCE_DOBLE_CACTUS:
                cactus_extra = cactus_small if random.random() < CHANCE_SEGUNDO_CACTUS_PEQUENO else cactus_imgs
                separacion = random.randint(SEPARACION_MIN, SEPARACION_MAX)
                obstaculos.add(Obstaculo(cactus_extra, ANCHO + separacion, ALTO, ALTURA_SUELO, velocidad_juego))
            tiempo_ultimo_obstaculo = tiempo_actual
            intervalo_cactus = random.randint(1000, 3000)

        # --- COLISIONES ---
        if pygame.sprite.spritecollide(jugador, obstaculos, False, pygame.sprite.collide_mask) or \
           pygame.sprite.spritecollide(jugador, aves, False, pygame.sprite.collide_mask):
            juego_activo = False
            record = max(record, int(puntaje))

        # --- PUNTAJE ---
        puntaje += 0.1
        if int(puntaje) % 100 == 0 and velocidad_juego < 15:
            velocidad_juego += 0.5

    # --- DIBUJAR ---
    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo.dibujar(VENTANA)
    obstaculos.draw(VENTANA)
    aves.draw(VENTANA)
    jugador.dibujar(VENTANA)
    VENTANA.blit(luna_img, luna_img.get_rect(topright=(ANCHO - 20, 20)))
    mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
    mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)

    if not juego_activo:
        VENTANA.blit(imagenes["game_over"], imagenes["game_over"].get_rect(center=(ANCHO // 2, ALTO // 2 - 30)))
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 90, BLANCO, VENTANA, centrado=True)
        mostrar_texto("Presiona ESC para volver al menú", ANCHO // 2, ALTO // 2 + 140, BLANCO, VENTANA, centrado=True)

    pygame.display.flip()
