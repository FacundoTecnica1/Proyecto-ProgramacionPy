import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo, Ave
from seleccion_personaje import SeleccionPersonaje
from utils import mostrar_texto
from menu import Menu
from seleccionar_mundo import SeleccionMundo
from seleccionar_sonido import SelectorSonido

pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 800, 550
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino Perro 🐶 / 🐱")

# --- RUTAS ---
RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")
RUTA_MUSICA = os.path.join(os.path.dirname(__file__), "..", "musica")

# --- COLORES ---
BLANCO = (255, 255, 255)
COLOR_ESPACIO_FONDO = (30, 30, 35)
ALTURA_SUELO = 30

# --- FUNCIONES ---
def cargar_imagen(nombre):
    return pygame.image.load(os.path.join(RUTA_BASE, nombre)).convert_alpha()

def escalar_lista(lista, w, h):
    return [pygame.transform.scale(img, (w, h)) for img in lista]

def reproducir_sonido(sonido, volumen):
    if sonido and volumen>0:
        sonido.set_volume(volumen)
        sonido.play()

# --- CARGA DE IMÁGENES ---
try:
    imagenes = {
        'perro_run': [cargar_imagen(f"perro_run{i}.png") for i in range(1,5)],
        'perro_jump': cargar_imagen("perro_jump.png"),
        'perro_air': cargar_imagen("perro_air.png"),
        'gato_run': [cargar_imagen(f"gato_run{i}.png") for i in range(1,5)],
        'gato_jump': cargar_imagen("gato_jump.png"),
        'gato_air': cargar_imagen("gato_air.png"),
        'cactus': [cargar_imagen(f"cactus{i}.png") for i in range(1,4)],
        'ave': [cargar_imagen(f"ave{i}.png") for i in range(1,4)],
        'fondo': cargar_imagen("fondo.png"),
        'luna': cargar_imagen("luna.png"),
        'game_over': cargar_imagen("game_over.png")
    }
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    pygame.quit()
    sys.exit()

# --- ESCALADO ---
imagenes['fondo'] = pygame.transform.scale(imagenes['fondo'], (ANCHO, ALTO))
luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))
perro_run = escalar_lista(imagenes['perro_run'], 150, 150)
gato_run = escalar_lista(imagenes['gato_run'], 150, 150)
perro_jump = pygame.transform.scale(imagenes['perro_jump'], (150,150))
perro_air = pygame.transform.scale(imagenes['perro_air'], (150,150))
gato_jump = pygame.transform.scale(imagenes['gato_jump'], (150,150))
gato_air = pygame.transform.scale(imagenes['gato_air'], (150,150))
cactus_imgs = escalar_lista(imagenes['cactus'], 110,140)
cactus_small = escalar_lista(imagenes['cactus'], 82,105)
ave_imgs = escalar_lista(imagenes['ave'], 100,80)

# --- SONIDOS ---
try:
    sonido_game_over = pygame.mixer.Sound(os.path.join(RUTA_MUSICA, "EfectoSonidoGameOver.mp3"))
except: sonido_game_over = None

try:
    sonido_salto = pygame.mixer.Sound(os.path.join(RUTA_MUSICA, "EfectoSonidoSalto.mp3"))
except: sonido_salto = None

# --- MENÚ PRINCIPAL ---
menu = Menu(VENTANA, ANCHO, ALTO, 0)

# --- SELECTOR DE SONIDO ---
selector_sonido = SelectorSonido(VENTANA, ANCHO, ALTO)
volumen_musica, volumen_sfx = selector_sonido.mostrar()
pygame.mixer.music.set_volume(volumen_musica)

# --- SELECCIÓN DE MUNDO ---
mundo_actual = "noche"
while True:
    opcion_menu = menu.mostrar()
    if opcion_menu == "jugar":
        break
    elif opcion_menu == "mundo":
        selector_mundo = SeleccionMundo(VENTANA, ANCHO, ALTO)
        mundo_seleccionado = selector_mundo.mostrar()
        if mundo_seleccionado in ("noche","dia"):
            mundo_actual = mundo_seleccionado
    elif opcion_menu == "sonido":
        volumen_musica, volumen_sfx = selector_sonido.mostrar()
        pygame.mixer.music.set_volume(volumen_musica)
    elif opcion_menu == "salir":
        pygame.quit()
        sys.exit()

# --- SELECCIÓN DE PERSONAJE ---
selector = SeleccionPersonaje(VENTANA, ANCHO, ALTO)
personaje = selector.mostrar()

# --- AJUSTE DEL MUNDO ---
sol_img = None
if mundo_actual=="dia":
    try:
        imagenes['fondo'] = pygame.transform.scale(cargar_imagen("fondo2.png"), (ANCHO, ALTO))
    except: pass
    try:
        imagenes['cactus'] = [cargar_imagen(f"cactus_verde{i}.png") for i in range(1,4)]
    except: pass
    try:
        sol_img = pygame.transform.scale(cargar_imagen("sol.png"), (80,80))
    except: pass

cactus_imgs = escalar_lista(imagenes['cactus'],110,140)
cactus_small = escalar_lista(imagenes['cactus'],82,105)

# --- CREAR JUGADOR ---
if personaje=="gato":
    jugador = Perro(gato_run,gato_jump,gato_air,ANCHO,ALTO,ALTURA_SUELO)
else:
    jugador = Perro(perro_run,perro_jump,perro_air,ANCHO,ALTO,ALTURA_SUELO)

# --- OBJETOS ---
fondo = Fondo(imagenes['fondo'],0.5)
obstaculos = pygame.sprite.Group()
aves = pygame.sprite.Group()

puntaje = 0
record = 0
juego_activo = True
velocidad_juego = 5.5
reloj = pygame.time.Clock()

tiempo_ultimo_obstaculo = pygame.time.get_ticks()
intervalo_cactus = random.randint(1000,3000)
tiempo_ultima_ave = pygame.time.get_ticks()
intervalo_ave = random.randint(4000,8000)

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
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                if jugador.en_suelo:
                    reproducir_sonido(sonido_salto, volumen_sfx)
                jugador.manejar_salto(event)
            else:
                jugador.manejar_salto(event)
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                jugador.reiniciar(ALTO,ALTURA_SUELO)
                obstaculos.empty()
                aves.empty()
                puntaje=0
                velocidad_juego=5.5
                juego_activo=True
                tiempo_ultimo_obstaculo=pygame.time.get_ticks()
                tiempo_ultima_ave=pygame.time.get_ticks()
                intervalo_cactus=random.randint(1000,3000)
                intervalo_ave=random.randint(4000,8000)
            elif event.key==pygame.K_ESCAPE:
                menu.record_actual=record
                if menu.mostrar()!="jugar":
                    pygame.quit()
                    sys.exit()

    # Actualizar música
    pygame.mixer.music.set_volume(volumen_musica)

    if juego_activo:
        fondo.actualizar(velocidad_juego)
        jugador.actualizar(dt)
        obstaculos.update()
        aves.update()
        tiempo_actual = pygame.time.get_ticks()

        # Aves
        if tiempo_actual - tiempo_ultima_ave > intervalo_ave:
            aves.add(Ave(ave_imgs, ANCHO, ALTO, velocidad_juego))
            tiempo_ultima_ave = tiempo_actual
            intervalo_ave = random.randint(4000,8000)

        # Cactus
        if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_cactus:
            obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
            if random.random() < CHANCE_DOBLE_CACTUS:
                cactus_extra = cactus_small if random.random()<CHANCE_SEGUNDO_CACTUS_PEQUENO else cactus_imgs
                separacion=random.randint(SEPARACION_MIN,SEPARACION_MAX)
                obstaculos.add(Obstaculo(cactus_extra,ANCHO+separacion,ALTO,ALTURA_SUELO,velocidad_juego))
            tiempo_ultimo_obstaculo=tiempo_actual
            intervalo_cactus=random.randint(1000,3000)

        # Colisiones
        if pygame.sprite.spritecollide(jugador,obstaculos,False,pygame.sprite.collide_mask) or \
           pygame.sprite.spritecollide(jugador,aves,False,pygame.sprite.collide_mask):
            juego_activo=False
            record=max(record,int(puntaje))
            pygame.mixer.stop()
            reproducir_sonido(sonido_game_over, volumen_sfx)

        # Puntaje
        puntaje+=0.1
        if int(puntaje)%100==0 and velocidad_juego<15:
            velocidad_juego+=0.5

    # --- DIBUJADO ---
    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo.dibujar(VENTANA)
    obstaculos.draw(VENTANA)
    aves.draw(VENTANA)
    jugador.dibujar(VENTANA)

    if mundo_actual=="dia" and sol_img is not None:
        VENTANA.blit(sol_img, sol_img.get_rect(topright=(ANCHO-20,20)))
    else:
        VENTANA.blit(luna_img, luna_img.get_rect(topright=(ANCHO-20,20)))

    mostrar_texto(f"Puntos: {int(puntaje)}",10,10,BLANCO,VENTANA)
    mostrar_texto(f"Record: {record}",ANCHO-150,10,BLANCO,VENTANA)

    if not juego_activo:
        VENTANA.blit(imagenes['game_over'], imagenes['game_over'].get_rect(center=(ANCHO//2, ALTO//2-30)))
        mostrar_texto("Presiona ESPACIO para reiniciar",ANCHO//2,ALTO//2+90,BLANCO,VENTANA,centrado=True)
        mostrar_texto("Presiona ESC para volver al menú",ANCHO//2,ALTO//2+140,BLANCO,VENTANA,centrado=True)

    pygame.display.flip()
