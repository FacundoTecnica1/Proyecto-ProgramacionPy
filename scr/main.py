import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo
from utils import mostrar_texto
from menu import Menu
import api_client 

def obtener_nombre_jugador(pantalla, ancho, alto):
    nombre = ""
    fuente = pygame.font.Font(None, 50)
    input_activo = True
    while input_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nombre:
                    input_activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 15:
                    nombre += event.unicode
        
        pantalla.fill((30, 30, 35))
        mostrar_texto("Ingresa tu nombre:", ancho // 2, alto // 2 - 50, (255, 255, 255), pantalla, 50, True)
        pygame.draw.rect(pantalla, (255, 255, 255), (ancho // 2 - 150, alto // 2 - 10, 300, 40), 2)
        texto_surface = fuente.render(nombre, True, (255, 255, 255))
        pantalla.blit(texto_surface, (ancho // 2 - 145, alto // 2))
        mostrar_texto("Presiona ENTER para continuar", ancho // 2, alto // 2 + 60, (200, 200, 200), pantalla, 30, True)
        pygame.display.flip()
    return nombre


pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 450
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino Perro 🐶")

RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_ESPACIO_FONDO = (30, 30, 35)

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
        'luna': pygame.image.load(os.path.join(RUTA_BASE, "luna.png")).convert_alpha()
    }
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    pygame.quit()
    sys.exit()

imagenes['fondo_completo'] = pygame.transform.scale(imagenes['fondo_completo'], (ANCHO, ALTO))

ALTURA_SUELO = 30
perro_corriendo_imgs = [pygame.transform.scale(img, (150, 150)) for img in imagenes['perro_corriendo']]
perro_salto_img = pygame.transform.scale(imagenes['perro_salto'], (150, 150))
perro_aire_img = pygame.transform.scale(imagenes['perro_aire'], (150, 150))
cactus_imgs = [pygame.transform.scale(img, (110, 140)) for img in imagenes['cactus']]
luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))

perro = Perro(perro_corriendo_imgs, perro_salto_img, perro_aire_img, ANCHO, ALTO, ALTURA_SUELO)
fondo_completo = Fondo(imagenes['fondo_completo'], 0.5)
obstaculos = pygame.sprite.Group()

puntaje = 0
record = api_client.obtener_record_online() # <-- CAMBIO: Obtenemos el récord del servidor
juego_activo = False
velocidad_juego = 5.5
tiempo_ultimo_obstaculo = pygame.time.get_ticks()
intervalo_proximo_cactus = random.randint(1000, 3000)

reloj = pygame.time.Clock()

menu = Menu(VENTANA, ANCHO, ALTO, record)
accion = menu.mostrar()

if accion == "jugar":
    juego_activo = True
else:
    pygame.quit()
    sys.exit()

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
                puntaje = 0
                juego_activo = True
                velocidad_juego = 5.5
                tiempo_ultimo_obstaculo = pygame.time.get_ticks()
                intervalo_proximo_cactus = random.randint(1000, 3000)
            elif event.key == pygame.K_ESCAPE:
                record = api_client.obtener_record_online() # <-- AÑADIDO: Actualizamos el récord antes de mostrar el menú
                menu.record_actual = record
                accion = menu.mostrar()
                if accion == "jugar": # Reiniciamos el juego si eligen "jugar"
                    perro.reiniciar(ALTO, ALTURA_SUELO)
                    obstaculos.empty()
                    puntaje = 0
                    juego_activo = True
                    velocidad_juego = 5.5
                else: # Si eligen otra opción, salimos (ya manejado en el menú)
                    pygame.quit()
                    sys.exit()

    if juego_activo:
        fondo_completo.actualizar(velocidad_juego)
        perro.actualizar(dt)
        obstaculos.update()

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_proximo_cactus:
            obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
            tiempo_ultimo_obstaculo = tiempo_actual
            intervalo_proximo_cactus = random.randint(1000, 3000)

        if pygame.sprite.spritecollide(perro, obstaculos, False, pygame.sprite.collide_mask):
            juego_activo = False
            # <-- CAMBIO: Lógica para guardar puntaje online
            nombre_jugador = obtener_nombre_jugador(VENTANA, ANCHO, ALTO)
            api_client.registrar_puntaje_online(nombre_jugador, int(puntaje))
            record = api_client.obtener_record_online() # Actualizamos el récord después de guardar

        puntaje += 0.1
        if int(puntaje) % 100 == 0 and velocidad_juego < 15:
            velocidad_juego += 0.5

    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo_completo.dibujar(VENTANA)
    obstaculos.draw(VENTANA)
    perro.dibujar(VENTANA)
    luna_rect = luna_img.get_rect(topright=(ANCHO - 20, 20))
    VENTANA.blit(luna_img, luna_rect)

    mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
    mostrar_texto(f"Record Global: {record}", ANCHO - 250, 10, BLANCO, VENTANA) # <-- CAMBIO: Texto actualizado

    if not juego_activo:
        game_over_rect = imagenes['game_over'].get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
        VENTANA.blit(imagenes['game_over'], game_over_rect)
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 90, BLANCO, VENTANA, centrado=True)
        mostrar_texto("Presiona ESC para volver al menú", ANCHO // 2, ALTO // 2 + 140, BLANCO, VENTANA, centrado=True)

    pygame.display.flip()