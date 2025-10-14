import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo, Ave
from seleccion_personaje import SeleccionPersonaje
from utils import mostrar_texto
from menu import Menu
from seleccionar_mundo import SeleccionMundo

pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 800, 600
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino")

# --- RUTA DE IMÁGENES ---
RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

# --- COLORES ---
BLANCO = (255, 255, 255)
COLOR_ESPACIO_FONDO = (30, 30, 35)
ALTURA_SUELO = 30

# --- FUNCIÓN PARA CARGAR IMÁGENES ---
def cargar_imagen(nombre):
    return pygame.image.load(os.path.join(RUTA_BASE, nombre)).convert_alpha()

# --- CARGA BASE DE IMÁGENES ---
try:
    imagenes = {
        'perro_run': [
            cargar_imagen("perro_run1.png"),
            cargar_imagen("perro_run2.png"),
            cargar_imagen("perro_run3.png"),
            cargar_imagen("perro_run4.png")
        ],
        'perro_jump': cargar_imagen("perro_jump.png"),
        'perro_air': cargar_imagen("perro_air.png"),

        'gato_run': [
            cargar_imagen("gato_run1.png"),
            cargar_imagen("gato_run2.png"),
            cargar_imagen("gato_run3.png"),
            cargar_imagen("gato_run4.png")
        ],
        'gato_jump': cargar_imagen("gato_jump.png"),
        'gato_air': cargar_imagen("gato_air.png"),

        'cactus': [
            cargar_imagen("cactus1.png"),
            cargar_imagen("cactus2.png"),
            cargar_imagen("cactus3.png")
        ],
        'ave': [
            cargar_imagen("ave1.png"),
            cargar_imagen("ave2.png"),
            cargar_imagen("ave3.png")
        ],
        'fondo': pygame.image.load(os.path.join(RUTA_BASE, "fondo.png")).convert(),
        'luna': cargar_imagen("luna.png"),
        'game_over': cargar_imagen("game_over.png")
    }
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    pygame.quit()
    sys.exit()

# --- ESCALAS ---
def escalar_lista(lista, w, h):
    return [pygame.transform.scale(img, (w, h)) for img in lista]

def escalar_y_cuadrar(img, size):
    w, h = img.get_size()
    scale = size / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    img_scaled = pygame.transform.smoothscale(img, (new_w, new_h))
    fondo = pygame.Surface((size, size), pygame.SRCALPHA)
    fondo.blit(img_scaled, ((size - new_w) // 2, (size - new_h) // 2))
    return fondo

def escalar_lista_cuadrada(lista, size):
    return [escalar_y_cuadrar(img, size) for img in lista]

imagenes['fondo'] = pygame.transform.scale(imagenes['fondo'], (ANCHO, ALTO))
luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))

perro_run = escalar_lista_cuadrada(imagenes["perro_run"], 150)
gato_run = escalar_lista_cuadrada(imagenes["gato_run"], 150)
perro_jump = escalar_y_cuadrar(imagenes["perro_jump"], 150)
perro_air = escalar_y_cuadrar(imagenes["perro_air"], 150)
gato_jump = escalar_y_cuadrar(imagenes["gato_jump"], 150)
gato_air = escalar_y_cuadrar(imagenes["gato_air"], 150)
cactus_imgs = escalar_lista_cuadrada(imagenes["cactus"], 140)
cactus_small = escalar_lista_cuadrada(imagenes["cactus"], 105)
ave_imgs = escalar_lista_cuadrada(imagenes["ave"], 100)

# --- MENÚ PRINCIPAL ---
menu = Menu(VENTANA, ANCHO, ALTO, 0)

# --- SELECCIÓN DE MUNDO ---
mundo_actual = "noche"  # por defecto
while True:
    opcion_menu = menu.mostrar()

    if opcion_menu == "jugar":
        break
    elif opcion_menu == "mundo":
        selector_mundo = SeleccionMundo(VENTANA, ANCHO, ALTO)
        mundo_seleccionado = selector_mundo.mostrar()
        if mundo_seleccionado in ("noche", "dia"):
            mundo_actual = mundo_seleccionado
    elif opcion_menu == "salir":
        pygame.quit()
        sys.exit()

# --- SELECCIÓN DE PERSONAJE ---
selector = SeleccionPersonaje(VENTANA, ANCHO, ALTO)
personaje = selector.mostrar()  # 'perro' o 'gato'

# --- CAMBIO DE ELEMENTOS SEGÚN EL MUNDO ---
sol_img = None
if mundo_actual == "dia":
    try:
        imagenes['fondo'] = pygame.transform.scale(cargar_imagen("fondo2.png"), (ANCHO, ALTO))
    except Exception as e:
        print(f"Advertencia: no se encontró fondo2.png -> usando fondo por defecto. ({e})")

    # ✅ CARGAR LOS CACTUS VERDES (solo cactus_verde1, 2 y 3)
    try:
        imagenes['cactus'] = [
            cargar_imagen("cactus_verde1.png"),
            cargar_imagen("cactus_verde2.png"),
            cargar_imagen("cactus_verde3.png")
        ]
    except Exception as e:
        print(f"Advertencia: no se encontraron cactus verdes, usando cactus normales. ({e})")
        imagenes['cactus'] = [
            cargar_imagen("cactus1.png"),
            cargar_imagen("cactus2.png"),
            cargar_imagen("cactus3.png")
        ]

    try:
        sol_img = pygame.transform.scale(cargar_imagen("sol.png"), (80, 80))
    except Exception as e:
        print(f"Advertencia: no se encontró sol.png. ({e})")
        sol_img = None
else:
    sol_img = None

# --- ESCALAR NUEVOS ELEMENTOS ---
cactus_imgs = escalar_lista(imagenes["cactus"], 110, 140)
cactus_small = escalar_lista(imagenes["cactus"], 82, 105)

# --- CREAR JUGADOR ---
if personaje == "gato":
    jugador = Perro(gato_run, gato_jump, gato_air, ANCHO, ALTO, ALTURA_SUELO)
else:
    jugador = Perro(perro_run, perro_jump, perro_air, ANCHO, ALTO, ALTURA_SUELO)

# --- OBJETOS DEL JUEGO ---
fondo = Fondo(imagenes["fondo"], 0.5)
obstaculos = pygame.sprite.Group()
aves = pygame.sprite.Group()

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

# --- BUCLE PRINCIPAL ---
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
                intervalo_cactus = random.randint(1000, 3000)
                intervalo_ave = random.randint(4000, 8000)
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

        # --- AVES ---
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

    # --- DIBUJADO ---
    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo.dibujar(VENTANA)
    obstaculos.draw(VENTANA)
    aves.draw(VENTANA)
    jugador.dibujar(VENTANA)

    if mundo_actual == "dia" and sol_img is not None:
        VENTANA.blit(sol_img, sol_img.get_rect(topright=(ANCHO - 20, 20)))
    else:
        VENTANA.blit(luna_img, luna_img.get_rect(topright=(ANCHO - 20, 20)))

    mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
    mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)

    if not juego_activo:
        VENTANA.blit(imagenes["game_over"], imagenes["game_over"].get_rect(center=(ANCHO // 2, ALTO // 2 - 30)))
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 90, BLANCO, VENTANA, centrado=True)
        mostrar_texto("Presiona ESC para volver al menú", ANCHO // 2, ALTO // 2 + 140, BLANCO, VENTANA, centrado=True)

    pygame.display.flip()
