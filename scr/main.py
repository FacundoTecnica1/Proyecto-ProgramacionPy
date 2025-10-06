import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo
from utils import mostrar_texto
from menu import Menu

# ===================== INICIALIZACIÓN =====================
pygame.init()
pygame.mixer.init()

ANCHO = 1000
ALTO = 600
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino Perro 🐶")

RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

BLANCO = (255, 255, 255)
COLOR_ESPACIO_FONDO = (30, 30, 35)
ALTURA_SUELO = 30

# ===================== CARGA PERSONAJE =====================
def cargar_personaje(tipo):
    run_imgs = []
    i = 1
    while True:
        ruta_run = os.path.join(RUTA_BASE, f"{tipo}_run{i}.png")
        if not os.path.exists(ruta_run):
            break
        run_imgs.append(pygame.image.load(ruta_run).convert_alpha())
        i += 1

    if not run_imgs:
        raise FileNotFoundError(f"No hay imágenes de corrida para '{tipo}' en {RUTA_BASE}")

    salto = pygame.image.load(os.path.join(RUTA_BASE, f"{tipo}_jump.png")).convert_alpha()
    aire = pygame.image.load(os.path.join(RUTA_BASE, f"{tipo}_air.png")).convert_alpha()

    run_imgs = [pygame.transform.scale(img, (150, 150)) for img in run_imgs]
    salto = pygame.transform.scale(salto, (150, 150))
    aire = pygame.transform.scale(aire, (150, 150))
    return run_imgs, salto, aire

# ===================== CARGA ESCENARIO =====================
try:
    imagenes = {
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
cactus_imgs = [pygame.transform.scale(img, (110, 140)) for img in imagenes['cactus']]
luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))

# ===================== LOOP DE JUEGO =====================
def jugar(personaje, record):
    imagenes_corriendo, imagen_salto, imagen_aire = cargar_personaje(personaje)
    jugador = Perro(imagenes_corriendo, imagen_salto, imagen_aire, ANCHO, ALTO, ALTURA_SUELO)
    fondo_completo = Fondo(imagenes['fondo_completo'], 0.5)
    obstaculos = pygame.sprite.Group()

    puntaje = 0.0
    velocidad_juego = 5.5
    tiempo_ultimo_obstaculo = pygame.time.get_ticks()
    intervalo_proximo_cactus = random.randint(1000, 3000)
    juego_activo = True
    reloj = pygame.time.Clock()

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
                    puntaje = 0.0
                    juego_activo = True
                    velocidad_juego = 5.5
                    tiempo_ultimo_obstaculo = pygame.time.get_ticks()
                    intervalo_proximo_cactus = random.randint(1000, 3000)

                elif event.key == pygame.K_ESCAPE:
                    return record

        # ===================== ACTUALIZACIÓN =====================
        if juego_activo:
            fondo_completo.actualizar(velocidad_juego)
            jugador.actualizar(dt)
            obstaculos.update()

            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_proximo_cactus:
                obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
                tiempo_ultimo_obstaculo = tiempo_actual
                intervalo_proximo_cactus = random.randint(1000, 3000)

            if pygame.sprite.spritecollide(jugador, obstaculos, False, pygame.sprite.collide_mask):
                juego_activo = False
                if puntaje > record:
                    record = int(puntaje)

            puntaje += 0.1
            if int(puntaje) % 100 == 0 and velocidad_juego < 15:
                velocidad_juego += 0.5

        # ===================== DIBUJADO =====================
        VENTANA.fill(COLOR_ESPACIO_FONDO)
        fondo_completo.dibujar(VENTANA)
        obstaculos.draw(VENTANA)
        jugador.dibujar(VENTANA)
        VENTANA.blit(luna_img, luna_img.get_rect(topright=(ANCHO - 20, 20)))

        mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
        mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)
        mostrar_texto(f"Personaje: {personaje.capitalize()}", ANCHO // 2, 10, BLANCO, VENTANA, centrado=True)

        if not juego_activo:
            game_over_rect = imagenes['game_over'].get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
            VENTANA.blit(imagenes['game_over'], game_over_rect)
            mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 90, BLANCO, VENTANA, centrado=True)
            mostrar_texto("Presiona ESC para volver al menú", ANCHO // 2, ALTO // 2 + 140, BLANCO, VENTANA, centrado=True)

        pygame.display.flip()

# ===================== MAIN LOOP =====================
def main():
    record = 0
    personaje = "perro"
    menu = Menu(VENTANA, ANCHO, ALTO, record)

    while True:
        accion, personaje = menu.mostrar()

        if accion == "jugar":
            record = jugar(personaje, record)
            menu.record_actual = record
        elif accion == "record":
            mostrar_texto(f"Récord actual: {record}", ANCHO // 2, ALTO // 2, BLANCO, VENTANA, centrado=True)
            pygame.display.flip()
            pygame.time.wait(1500)
        elif accion == "salir":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
