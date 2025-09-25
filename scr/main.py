import pygame
import random
import sys
import os

from game_objects import Perro, Obstaculo, Fondo, Portal, Boss, BolaFuego # Importa las nuevas clases
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
pygame.display.set_caption("Dino")

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
        'portal': [
            pygame.image.load(os.path.join(RUTA_BASE, "portal1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "portal2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "portal3.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "portal4.png")).convert_alpha()
        ],
        # --- NUEVO: Imágenes del BOSS ---
        'boss': [
            pygame.image.load(os.path.join(RUTA_BASE, "boss1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "boss2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "boss3.png")).convert_alpha()
        ],
        # --- NUEVO: Imágenes de la BOLA DE FUEGO ---
        'bola_fuego': [
            pygame.image.load(os.path.join(RUTA_BASE, "bola1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "bola2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "bola3.png")).convert_alpha(),
            pygame.image.load(os.path.join(RUTA_BASE, "bola4.png")).convert_alpha()
        ]
    }

except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    pygame.quit()
    sys.exit()

imagenes['fondo_completo'] = pygame.transform.scale(imagenes['fondo_completo'], (ANCHO, ALTO))

# ==============================
# VARIABLES DEL JUEGO
# ==============================
ALTURA_SUELO = 30

perro_corriendo_imgs = [pygame.transform.scale(img, (150, 150)) for img in imagenes['perro_corriendo']]
perro_salto_img = pygame.transform.scale(imagenes['perro_salto'], (150, 150))
perro_aire_img = pygame.transform.scale(imagenes['perro_aire'], (150, 150))
cactus_imgs = [pygame.transform.scale(img, (110, 140)) for img in imagenes['cactus']]
luna_img = pygame.transform.scale(imagenes['luna'], (75, 75))
portal_imgs = [pygame.transform.scale(img, (120, 180)) for img in imagenes['portal']]

# --- NUEVO: Escalar imágenes del jefe y bola de fuego ---
boss_imgs = [pygame.transform.scale(img, (150, 150)) for img in imagenes['boss']]
bola_fuego_imgs = [pygame.transform.scale(img, (50, 50)) for img in imagenes['bola_fuego']] # Ajustar tamaño

perro = Perro(perro_corriendo_imgs, perro_salto_img, perro_aire_img, ANCHO, ALTO, ALTURA_SUELO)
fondo_completo = Fondo(imagenes['fondo_completo'], 0.5) 
obstaculos = pygame.sprite.Group()
portales = pygame.sprite.Group() 
bolas_fuego = pygame.sprite.Group() # Grupo para las bolas de fuego

# --- NUEVO: Variables del modo BOSS ---
modo_boss = False
boss = None
boss_generado = False # Para asegurar que se crea el jefe solo una vez

puntaje = 0
record = 0
juego_activo = True
velocidad_juego = 5.5
tiempo_ultimo_obstaculo = pygame.time.get_ticks()

reloj = pygame.time.Clock()
intervalo_proximo_cactus = random.randint(1000, 3000)

cactus_generados_desde_ultimo_portal = 0
portal_generado_en_ciclo = False

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
            portales.empty()
            bolas_fuego.empty() # Limpiar bolas de fuego
            
            # Reiniciar variables de BOSS
            modo_boss = False
            boss = None
            boss_generado = False
            
            puntaje = 0
            record = 0
            juego_activo = True
            velocidad_juego = 5.5
            tiempo_ultimo_obstaculo = pygame.time.get_ticks()
            intervalo_proximo_cactus = random.randint(1000, 3000)
            cactus_generados_desde_ultimo_portal = 0
            portal_generado_en_ciclo = False

    if juego_activo:
        
        # Actualización de elementos
        fondo_completo.actualizar(velocidad_juego, modo_boss) # Fondo se detiene en modo boss
        perro.actualizar(dt, modo_boss) # Perro se actualiza diferente en modo boss
        
        if not modo_boss:
            obstaculos.update()
            portales.update(dt)
            
            # Lógica de generación de obstáculos y portal (Modo Normal)
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_proximo_cactus:
                if cactus_generados_desde_ultimo_portal < 4:
                    obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
                    cactus_generados_desde_ultimo_portal += 1
                    portal_generado_en_ciclo = False
                elif not portal_generado_en_ciclo:
                    portales.add(Portal(portal_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
                    cactus_generados_desde_ultimo_portal = 0
                    portal_generado_en_ciclo = True
                
                tiempo_ultimo_obstaculo = tiempo_actual
                intervalo_proximo_cactus = random.randint(1000, 3000)

            # Colisión con obstáculos (Modo Normal)
            if pygame.sprite.spritecollide(perro, obstaculos, False, pygame.sprite.collide_mask):
                juego_activo = False
                if puntaje > record:
                    record = int(puntaje)

            # Colisión con el portal -> Activa Modo Boss
            for portal in pygame.sprite.spritecollide(perro, portales, True, pygame.sprite.collide_mask): # Eliminar portal
                if not modo_boss:
                    puntaje += 50
                    print("¡Has pasado por el portal! ¡Modo Boss Activado!")
                    modo_boss = True
                    obstaculos.empty() # Eliminar cualquier cactus restante
                    portales.empty() # Asegurar que no quede el portal
                    boss = Boss(boss_imgs, ANCHO, ALTO, ALTURA_SUELO)
                    boss_generado = True
                    
            puntaje += 0.1
            if int(puntaje) % 100 == 0 and velocidad_juego < 15:
                velocidad_juego += 0.5
                
        else: # Modo Boss Activo
            boss.update(dt)
            bolas_fuego.update()
            
            # Lógica de ataque del Boss
            if boss.debe_atacar():
                # Generar bola de fuego en la posición de la mano del jefe, usando su índice de animación
                pos_inicio_bola = boss.obtener_posicion_bola()
                indice_bola = boss.get_current_bola_img_index()
                
                # Usaremos la imagen de bola que corresponde al frame del jefe (bola1 con boss1, etc.)
                bolas_fuego.add(BolaFuego(bola_fuego_imgs, indice_bola, pos_inicio_bola, velocidad_juego)) 
                
            # Colisión con bolas de fuego
            if pygame.sprite.spritecollide(perro, bolas_fuego, True, pygame.sprite.collide_mask):
                juego_activo = False # Game Over
                print("¡Impacto de Bola de Fuego! Game Over.")
                if puntaje > record:
                    record = int(puntaje)


        # --- Dibujo ---
        VENTANA.fill(COLOR_ESPACIO_FONDO)
        fondo_completo.dibujar(VENTANA)
        
        if modo_boss and boss:
            VENTANA.blit(boss.image, boss.rect)
            bolas_fuego.draw(VENTANA)
        else:
            obstaculos.draw(VENTANA)
            portales.draw(VENTANA)
            
        perro.dibujar(VENTANA)
        luna_rect = luna_img.get_rect(topright=(ANCHO - 20, 20))
        VENTANA.blit(luna_img, luna_rect)

        mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
        mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)
        if modo_boss:
            mostrar_texto("¡MODO BOSS!", ANCHO // 2, 50, (255, 50, 50), VENTANA, centrado=True)

    if not juego_activo:
        game_over_rect = imagenes['game_over'].get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
        VENTANA.blit(imagenes['game_over'], game_over_rect)
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 90, BLANCO, VENTANA, centrado=True)
        mostrar_texto(f"Tu puntuación: {int(puntaje)}", ANCHO // 2, ALTO // 2 + 120, BLANCO, VENTANA, centrado=True)
        mostrar_texto(f"Record: {record}", ANCHO // 2, ALTO // 2 + 150, BLANCO, VENTANA, centrado=True)

    pygame.display.flip()