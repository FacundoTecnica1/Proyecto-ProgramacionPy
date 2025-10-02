import pygame
import random
import sys
import os

# ### MODIFICADO ###: Importamos la nueva clase Ave
from game_objects import Perro, Obstaculo, Fondo, Ave
from utils import mostrar_texto
from menu import Menu


pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 450
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino Perro ")


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
        'luna': pygame.image.load(os.path.join(RUTA_BASE, "luna.png")).convert_alpha(),
        ### NUEVO ###: Cargamos las imágenes del ave
        'ave': [
            pygame.image.load(os.path.join(RUTA_BASE, "ave1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "ave2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "ave3.png")).convert_alpha()
        ]
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

ANCHO_CACTUS_PEQ = int(110 * 0.75)
ALTO_CACTUS_PEQ = int(140 * 0.75)
cactus_pequeno_imgs = [pygame.transform.scale(img, (ANCHO_CACTUS_PEQ, ALTO_CACTUS_PEQ)) for img in imagenes['cactus']]

luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))

### NUEVO ###: Redimensionamos las imágenes del ave
ave_imgs = [pygame.transform.scale(img, (100, 80)) for img in imagenes['ave']]


perro = Perro(perro_corriendo_imgs, perro_salto_img, perro_aire_img, ANCHO, ALTO, ALTURA_SUELO)
fondo_completo = Fondo(imagenes['fondo_completo'], 0.5)
obstaculos = pygame.sprite.Group()
### NUEVO ###: Creamos un grupo de sprites para las aves
aves = pygame.sprite.Group()

puntaje = 0
record = 0
juego_activo = False
velocidad_juego = 5.5
tiempo_ultimo_obstaculo = pygame.time.get_ticks()
intervalo_proximo_cactus = random.randint(1000, 3000)

### NUEVO ###: Variable para controlar cuándo debe aparecer la próxima ave
puntaje_objetivo_ave = 200

CHANCE_DOBLE_CACTUS = 0.5 
SEPARACION_DOBLE_CACTUS_MIN = 60
SEPARACION_DOBLE_CACTUS_MAX = 90
CHANCE_SEGUNDO_CACTUS_PEQUENO = 0.9

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
                ### NUEVO ###: Limpiamos las aves al reiniciar
                aves.empty()
                puntaje = 0
                juego_activo = True
                velocidad_juego = 5.5
                tiempo_ultimo_obstaculo = pygame.time.get_ticks()
                intervalo_proximo_cactus = random.randint(1000, 3000)
                ### NUEVO ###: Reiniciamos el puntaje objetivo para el ave
                puntaje_objetivo_ave = 200
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
        ### NUEVO ###: Actualizamos las aves
        aves.update()

        ### NUEVO ###: Lógica para generar el ave cada 200 puntos
        if puntaje >= puntaje_objetivo_ave:
            aves.add(Ave(ave_imgs, ANCHO, ALTO, velocidad_juego))
            puntaje_objetivo_ave += 200 # El próximo aparecerá en 400, 600, etc.

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_proximo_cactus:
            obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
            if random.random() < CHANCE_DOBLE_CACTUS:
                if random.random() < CHANCE_SEGUNDO_CACTUS_PEQUENO:
                    imagenes_segundo_cactus = cactus_pequeno_imgs
                    separacion = random.randint(SEPARACION_DOBLE_CACTUS_MIN, SEPARACION_DOBLE_CACTUS_MAX)
                else:
                    imagenes_segundo_cactus = cactus_imgs
                    separacion = random.randint(SEPARACION_DOBLE_CACTUS_MIN + 20, SEPARACION_DOBLE_CACTUS_MAX + 40)
                obstaculos.add(Obstaculo(imagenes_segundo_cactus, ANCHO + separacion, ALTO, ALTURA_SUELO, velocidad_juego))
            
            tiempo_ultimo_obstaculo = tiempo_actual
            intervalo_proximo_cactus = random.randint(1000, 3000)

        ### MODIFICADO ###: Comprobamos colisión con cactus O con aves
        colision_cactus = pygame.sprite.spritecollide(perro, obstaculos, False, pygame.sprite.collide_mask)
        colision_ave = pygame.sprite.spritecollide(perro, aves, False, pygame.sprite.collide_mask)
        
        if colision_cactus or colision_ave:
            juego_activo = False
            if puntaje > record:
                record = int(puntaje)

        puntaje += 0.1
        if int(puntaje) % 100 == 0 and velocidad_juego < 15:
            velocidad_juego += 0.5


    VENTANA.fill(COLOR_ESPACIO_FONDO)
    fondo_completo.dibujar(VENTANA)
    obstaculos.draw(VENTANA)
    ### NUEVO ###: Dibujamos las aves en la ventana
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