import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# --- Constantes de pantalla ---
ANCHO, ALTO = 800, 500
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cactus Simplificado")

# --- Cargar y escalar imágenes ---
# Nota: Asegúrate de que las imágenes 'dino.png' y 'cactus.png' existan en la carpeta 'img'
# Usaremos solo un tipo de cactus para simplificar
try:
    fondo_img = pygame.image.load("img/fondo.png").convert()
    fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
    dino_img = pygame.image.load("img/dino.png").convert_alpha()
    dino_img = pygame.transform.scale(dino_img, (80, 80))
    cactus_img = pygame.image.load("img/cactus1.png").convert_alpha()
    cactus_img = pygame.transform.scale(cactus_img, (60, 100))
    game_over_img = pygame.image.load("img/gameover.png").convert_alpha()
    game_over_img = pygame.transform.scale(game_over_img, (300, 300))
except pygame.error as e:
    print(f"Error al cargar una imagen: {e}")
    sys.exit()

# --- Parámetros del Juego ---
FPS = 60
VELOCIDAD_JUEGO = 8
GRAVEDAD = 1.2

# --- Jugador (Dino) ---
dino_rect = dino_img.get_rect(topleft=(50, ALTO - 80))
saltando = False
velocidad_salto = -15

# --- Obstáculos (Cactus) ---
obstaculos = []
tiempo_ultimo_cactus = pygame.time.get_ticks()
INTERVALO_CACTUS = 1500  # milisegundos

# --- Puntuación ---
puntuacion = 0
fuente = pygame.font.Font(None, 36)

def generar_cactus():
    """Crea un nuevo cactus y lo añade a la lista de obstáculos."""
    nuevo_cactus = cactus_img.get_rect(topleft=(ANCHO, ALTO - 100))
    obstaculos.append(nuevo_cactus)

def dibujar_elementos():
    """Dibuja todos los elementos en la pantalla."""
    PANTALLA.blit(fondo_img, (0, 0))
    PANTALLA.blit(dino_img, dino_rect)
    for cactus in obstaculos:
        PANTALLA.blit(cactus_img, cactus)
    
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (0, 0, 0))
    PANTALLA.blit(texto_puntuacion, (10, 10))
    pygame.display.flip()

def main():
    """Función principal del juego."""
    global saltando, velocidad_salto, puntuacion, tiempo_ultimo_cactus

    en_juego = True
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # Salto del dino
                if evento.key == pygame.K_SPACE and not saltando and en_juego:
                    saltando = True
                    velocidad_salto = -15
                
                # Reiniciar el juego
                if evento.key == pygame.K_r and not en_juego:
                    main() # Reinicia el juego llamando a la función principal de nuevo
                    return # Finaliza esta ejecución de la función

        if en_juego:
            # Lógica de Salto
            if saltando:
                dino_rect.y += velocidad_salto
                velocidad_salto += GRAVEDAD
                if dino_rect.bottom >= ALTO - 20: # 20px de margen para el suelo
                    dino_rect.bottom = ALTO - 20
                    saltando = False
            
            # Generar nuevos cactus
            ahora = pygame.time.get_ticks()
            if ahora - tiempo_ultimo_cactus > INTERVALO_CACTUS + random.randint(0, 500):
                generar_cactus()
                tiempo_ultimo_cactus = ahora

            # Mover y eliminar cactus
            for cactus in obstaculos:
                cactus.x -= VELOCIDAD_JUEGO
            
            obstaculos[:] = [cactus for cactus in obstaculos if cactus.right > 0]
            
            # Colisión y fin del juego
            for cactus in obstaculos:
                if dino_rect.colliderect(cactus):
                    en_juego = False
            
            # Actualizar puntuación
            for cactus in obstaculos:
                if cactus.right < dino_rect.left and not cactus.colliderect(dino_rect):
                    puntuacion = len([c for c in obstaculos if c.right < dino_rect.left])

            dibujar_elementos()
        else:
            # Pantalla de Game Over
            PANTALLA.blit(game_over_img, ((ANCHO - 300) // 2, (ALTO - 300) // 2))
            texto_reiniciar = fuente.render("Presiona R para reiniciar", True, (255, 255, 255))
            PANTALLA.blit(texto_reiniciar, ((ANCHO - texto_reiniciar.get_width()) // 2, (ALTO // 2) + 100))
            pygame.display.flip()

if __name__ == "__main__":
    main()