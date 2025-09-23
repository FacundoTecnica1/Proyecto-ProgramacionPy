import pygame
import random
import sys
import os # Para manejar rutas de archivos

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
pygame.init()
pygame.mixer.init()

ANCHO = 800
ALTO = 450
FPS = 60

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Corredor Lunar")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_OSCURO = (50, 50, 50)

# Fuente
fuente = pygame.font.SysFont("Arial", 28)

# ==============================
# CARGA DE IMÁGENES
# ==============================
# Usamos os.path.join para compatibilidad de rutas
ruta_base = "img"
# Escalar imágenes
PERRO_ANCHO = 80 # Ajustado para que se vea bien
PERRO_ALTO = 80
CACTUS_ANCHO = 120
CACTUS_ALTO = 150 
try:
    # Cargar las imágenes de la animación del perro
    perro_corriendo_imgs = [
        pygame.image.load(os.path.join(ruta_base, "perro_run1.png")).convert_alpha(),
        pygame.image.load(os.path.join(ruta_base, "perro_run2.png")).convert_alpha(),
        pygame.image.load(os.path.join(ruta_base, "perro_run3.png")).convert_alpha(),
        pygame.image.load(os.path.join(ruta_base, "perro_run4.png")).convert_alpha()
    ]
    
    # Escalar todas las imágenes de la animación
    perro_corriendo_imgs = [pygame.transform.scale(img, (PERRO_ANCHO, PERRO_ALTO)) for img in perro_corriendo_imgs]
    cactus_imgs = [
        pygame.image.load(os.path.join(ruta_base, "cactus1.png")).convert_alpha(),
        pygame.image.load(os.path.join(ruta_base, "cactus2.png")).convert_alpha(),
        pygame.image.load(os.path.join(ruta_base, "cactus3.png")).convert_alpha() # Usamos Image 8 como tercer cactus
    ]
    fondo_lunar_img = pygame.image.load(os.path.join(ruta_base, "fondo.png")).convert()
    game_over_img = pygame.image.load(os.path.join(ruta_base, "game_over.png")).convert_alpha()
    luna_alien_img = pygame.image.load(os.path.join(ruta_base, "luna.png")).convert_alpha()
    suelo_fondo_img = pygame.image.load(os.path.join(ruta_base, "suelo_fondo.png")).convert() # Image 7 para el horizonte
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    print("Asegúrate de que las imágenes 'perro.png', 'cactus1.png', 'cactus2.png', 'cactus3.png', 'fondo_lunar.png', 'game_over.png', 'luna_alien.png', 'suelo_fondo.png' estén en la carpeta 'img'.")
    sys.exit()

# Variables para la animación del perro
indice_animacion_perro = 0
tiempo_animacion_perro = 0
velocidad_animacion_perro = 100 # Cambiar de frame cada 100 ms (ajusta a tu gusto)

# Cuando el perro salta, podrías usar una imagen estática de salto
perro_salto_img = perro_corriendo_imgs[0] # O cargar una imagen específica para salto si la tienes

# Escalar imágenes
PERRO_ANCHO = 80 # Ajustado para que se vea bien
PERRO_ALTO = 80

CACTUS_ANCHO = 120
CACTUS_ALTO = 150 # Un poco más alto para que se vea bien
cactus_imgs = [pygame.transform.scale(img, (CACTUS_ANCHO, CACTUS_ALTO)) for img in cactus_imgs]

# Escalar fondo lunar para que quepa en el ancho
fondo_lunar_img = pygame.transform.scale(fondo_lunar_img, (ANCHO, ALTO))

# Escalar y posicionar Game Over
GAME_OVER_ANCHO = 200
GAME_OVER_ALTO = 70
game_over_img = pygame.transform.scale(game_over_img, (GAME_OVER_ANCHO, GAME_OVER_ALTO))
game_over_rect = game_over_img.get_rect(center=(ANCHO // 2, ALTO // 2 - 30))

# Escalar luna con alien
LUNA_ANCHO = 100
LUNA_ALTO = 100
luna_alien_img = pygame.transform.scale(luna_alien_img, (LUNA_ANCHO, LUNA_ALTO))
luna_alien_rect = luna_alien_img.get_rect(topright=(ANCHO - 20, 20)) # Posición inicial

# Escalar y repetir suelo_fondo
SUELO_FONDO_ALTO = 60 # Ajustado para que se vea como el horizonte/suelo del fondo
suelo_fondo_img = pygame.transform.scale(suelo_fondo_img, (ANCHO, SUELO_FONDO_ALTO))


# ==============================
# VARIABLES DEL JUEGO
# ==============================
# Perro
perro_x = 50
ALTURA_SUELO = 60
# Usa PERRO_ALTO directamente
perro_y = ALTO - ALTURA_SUELO - PERRO_ALTO
perro_vel_y = 0
gravedad = 1.2
en_suelo = True

# Obstáculos
obstaculos = []
velocidad_juego = 6 # Velocidad inicial
tiempo_ultimo_obstaculo = 0
tiempo_entre_obstaculos = 1500  # ms

# Puntuación
puntaje = 0
record = 0
juego_activo = True

# Fondo en movimiento
fondo_x = 0
suelo_x = 0
luna_x = ANCHO - 20 # Posición inicial de la luna
luna_y = 20
luna_velocidad = 0.5 # Velocidad de la luna (más lenta que el suelo)

# Reloj
clock = pygame.time.Clock()

# ==============================
# FUNCIONES
# ==============================
def mostrar_texto(texto, x, y, color=NEGRO, tamaño=28, centrado=False):
    fuente_local = pygame.font.SysFont("Arial", tamaño)
    render = fuente_local.render(texto, True, color)
    if centrado:
        render_rect = render.get_rect(center=(x, y))
        ventana.blit(render, render_rect)
    else:
        ventana.blit(render, (x, y))

def reiniciar_juego():
    global perro_y, perro_vel_y, en_suelo, obstaculos, puntaje, juego_activo, velocidad_juego, fondo_x, suelo_x, luna_x, luna_y
    perro_y = ALTO - ALTURA_SUELO - PERRO_ALTO
    perro_vel_y = 0
    en_suelo = True
    obstaculos.clear()
    puntaje = 0
    juego_activo = True
    velocidad_juego = 6
    fondo_x = 0
    suelo_x = 0
    luna_x = ANCHO - 20
    luna_y = 20


def crear_obstaculo():
    img_cactus = random.choice(cactus_imgs)
    rect = img_cactus.get_rect()
    rect.x = ANCHO + random.randint(0, 100) # Un poco de variación en el punto de aparición
    rect.y = ALTO - ALTURA_SUELO - rect.height
    return {'rect': rect, 'img': img_cactus} # Guardamos la imagen con su rect

# ==============================
# BUCLE PRINCIPAL
# ==============================
while True:
    dt = clock.tick(FPS)
    
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
                    perro_vel_y = -18 # Fuerza de salto
                    en_suelo = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reiniciar_juego()

    # --------------------------
    # ACTUALIZACIONES DEL JUEGO
    # --------------------------
    if juego_activo:
        # Movimiento de fondo lunar
        fondo_x -= velocidad_juego * 0.2 # Se mueve más lento que los objetos en primer plano
        if fondo_x <= -ANCHO:
            fondo_x = 0

        # Movimiento del suelo/horizonte (Image 7)
        suelo_x -= velocidad_juego * 0.8 # Se mueve un poco más lento que los obstáculos
        if suelo_x <= -ANCHO:
            suelo_x = 0

        # Movimiento de la luna
        luna_x -= luna_velocidad
        if luna_x + LUNA_ANCHO < 0:
            luna_x = ANCHO + random.randint(0, ANCHO // 2) # Reaparece en un punto aleatorio fuera de la pantalla
            luna_y = random.randint(20, ALTO // 4) # Variar altura

        # Movimiento del perro
        perro_vel_y += gravedad
        perro_y += perro_vel_y

        # Limitar al suelo
        if perro_y >= ALTO - ALTURA_SUELO - PERRO_ALTO: # Usa PERRO_ALTO directamente
            perro_y = ALTO - ALTURA_SUELO - PERRO_ALTO
            en_suelo = True
            perro_vel_y = 0

        # Lógica de animación del perro (cuando está en el suelo)
        if en_suelo:
            tiempo_animacion_perro += dt
            if tiempo_animacion_perro >= velocidad_animacion_perro:
                indice_animacion_perro = (indice_animacion_perro + 1) % len(perro_corriendo_imgs)
                tiempo_animacion_perro = 0
            perro_img_actual = perro_corriendo_imgs[indice_animacion_perro]
        else: # Si está en el aire (saltando)
            perro_img_actual = perro_salto_img # Usa la imagen de salto

        # Generar obstáculos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_obstaculo > tiempo_entre_obstaculos:
            obstaculos.append(crear_obstaculo())
            tiempo_ultimo_obstaculo = tiempo_actual
            # Aumentar dificultad gradualmente
            if velocidad_juego < 15:
                velocidad_juego += 0.05
            if tiempo_entre_obstaculos > 800:
                tiempo_entre_obstaculos -= 5 # Reducir el tiempo entre obstáculos

        # Mover y dibujar obstáculos
        for obs in obstaculos:
            obs['rect'].x -= velocidad_juego
            
        # Eliminar obstáculos que salen de la pantalla
        obstaculos = [o for o in obstaculos if o['rect'].x + o['rect'].width > 0]

        # Detección de colisiones
        perro_rect = pygame.Rect(perro_x, perro_y, PERRO_ANCHO * 0.8, PERRO_ALTO * 0.9)
        perro_rect.centerx = perro_x + PERRO_ANCHO // 2
        perro_rect.bottom = perro_y + PERRO_ALTO
        
        for obs in obstaculos:
            if perro_rect.colliderect(obs['rect']):
                juego_activo = False
                if puntaje > record:
                    record = int(puntaje)

        # Actualizar puntuación
        puntaje += 0.1

    # --------------------------
    # DIBUJAR EN PANTALLA
    # --------------------------
    ventana.fill(BLANCO)

    # Dibujar fondo lunar en movimiento
    ventana.blit(fondo_lunar_img, (fondo_x, 0))
    ventana.blit(fondo_lunar_img, (fondo_x + ANCHO, 0)) # Para un desplazamiento continuo

    # Dibujar la luna con el alien
    ventana.blit(luna_alien_img, (luna_x, luna_y))

    # Dibujar el suelo (la franja de la Image 7)
    ventana.blit(suelo_fondo_img, (suelo_x, ALTO - ALTURA_SUELO))
    ventana.blit(suelo_fondo_img, (suelo_x + ANCHO, ALTO - ALTURA_SUELO)) # Para desplazamiento continuo

    # Dibujar la línea de suelo
    pygame.draw.rect(ventana, NEGRO, (0, ALTO - ALTURA_SUELO, ANCHO, ALTURA_SUELO))


    if juego_activo:
        # Dibujar obstáculos
        for obs in obstaculos:
            ventana.blit(obs['img'], obs['rect'])

        # Dibujar perro
        ventana.blit(perro_img_actual, (perro_x, perro_y))

        # HUD
        mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO)
        mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO) # Se muestra en el fondo oscuro
    else:
        # Pantalla de Game Over
        ventana.blit(game_over_img, game_over_rect)
        mostrar_texto("Presiona ESPACIO para reiniciar", ANCHO // 2, ALTO // 2 + 50, NEGRO, 24, centrado=True)
        mostrar_texto(f"Tu puntuación: {int(puntaje)}", ANCHO // 2, ALTO // 2 + 80, NEGRO, 20, centrado=True)
        mostrar_texto(f"Record: {record}", ANCHO // 2, ALTO // 2 + 100, NEGRO, 20, centrado=True)


    pygame.display.flip()