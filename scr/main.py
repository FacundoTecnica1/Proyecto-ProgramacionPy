import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes de pantalla
ANCHO, ALTO = 500, 300
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Cactus")

# Cargar imágenes y escalar a 500x300 o dimensiones adecuadas
fondo = pygame.image.load("imagenes/fondo.png").convert_alpha()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

game_over_img = pygame.image.load("imagenes/gameover.png").convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (300, 300))

jugador_img = pygame.image.load("imagenes/dino.png").convert_alpha()
jugador_img = pygame.transform.scale(jugador_img, (80, 80))

cactus1_img = pygame.image.load("imagenes/cactus1.png").convert_alpha()
cactus1_img = pygame.transform.scale(cactus1_img, (60, 100))

cactus2_img = pygame.image.load("imagenes/cactus2.png").convert_alpha()
cactus2_img = pygame.transform.scale(cactus2_img, (50, 80))

# FPS y reloj
FPS = 60
reloj = pygame.time.Clock()

# --- Parámetros del Jugador ---
jugador_x = 50
jugador_y_suelo = ALTO - 80
jugador_ancho = 80
jugador_altura = 80
vel_salto = 15
gravedad = 1

# --- Parámetros de los Obstáculos ---
vel_obstaculo = 10
ultimo_cactus = None

# --- Parámetros de Colisión ---
ancho_rect_jugador = 30
alto_rect_jugador = 40
offset_x_colision = 5
offset_y_colision = 10

# --- Variables del Juego ---
jugador_y = jugador_y_suelo
saltando = False
vel_y = 0

puntuacion = 0

# Fuente para el puntaje
fuente = pygame.font.SysFont(None, 24)

def dibujar():
    PANTALLA.blit(fondo, (0, 0))
    PANTALLA.blit(jugador_img, (jugador_x, jugador_y))
    for obs in obstaculos:
        PANTALLA.blit(obs[0], (obs[1], obs[2]))
    puntaje_text = fuente.render(f"Puntaje: {puntuacion}", True, (0,0,0))
    PANTALLA.blit(puntaje_text, (10, 10))
    pygame.display.update()

def pantalla_game_over():
    PANTALLA.fill((0,0,0))
    PANTALLA.blit(game_over_img, ((ANCHO - 300)//2, (ALTO - 80)//2))
    mensaje_reinicio = fuente.render("Presiona R para reiniciar o ESC para salir", True, (255, 255, 255))
    PANTALLA.blit(mensaje_reinicio, ((ANCHO - mensaje_reinicio.get_width())//2, (ALTO - 80)//2 + 100))
    pygame.display.update()

def main():
    global jugador_y, saltando, vel_y, puntuacion, obstaculos, ultimo_cactus

    corriendo = True
    en_game_over = False

    obstaculos = []
    puntuacion = 0
    jugador_y = jugador_y_suelo
    saltando = False
    vel_y = 0

    primer_cactus = random.choice([cactus1_img, cactus2_img])
    obstaculos.append([primer_cactus, ANCHO, ALTO - primer_cactus.get_height() + 20])
    ultimo_cactus = primer_cactus

    while corriendo:
        reloj.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            
            if en_game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                        return
                    elif event.key == pygame.K_ESCAPE:
                        corriendo = False
        
        keys = pygame.key.get_pressed()

        if not en_game_over:
            if keys[pygame.K_ESCAPE]:
                corriendo = False

            # Lógica de Salto
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not saltando:
                saltando = True
                vel_y = -vel_salto
            
            if saltando:
                jugador_y += vel_y
                vel_y += gravedad

            if jugador_y >= jugador_y_suelo:
                jugador_y = jugador_y_suelo
                saltando = False
                vel_y = 0
            
            # Mover obstáculos
            for obs in obstaculos:
                obs[1] -= vel_obstaculo

            # Eliminar obstáculos y agregar nuevos
            if obstaculos and obstaculos[0][1] < -50:
                obstaculos.pop(0)
                puntuacion += 1
                
                # Generar dos cactus juntos con un 15% de probabilidad
                if random.random() < 0.15:
                    cactus1 = cactus1_img
                    cactus2 = cactus2_img
                    if cactus1 == cactus2:
                        cactus2 = cactus1_img if cactus2 == cactus2_img else cactus2_img

                    obstaculos.append([cactus1, ANCHO + random.randint(100, 200), ALTO - cactus1.get_height() + 20])
                    # El segundo cactus se genera muy cerca del primero
                    obstaculos.append([cactus2, obstaculos[0][1] + random.randint(30, 80), ALTO - cactus2.get_height() + 20])
                else:
                    # Alternar la generación de cactus
                    if ultimo_cactus == cactus1_img:
                        nuevo_cactus = cactus2_img
                    else:
                        nuevo_cactus = cactus1_img
                    
                    obstaculos.append([nuevo_cactus, ANCHO + random.randint(100, 300), ALTO - nuevo_cactus.get_height() + 20])
                
                ultimo_cactus = obstaculos[-1][0]
            
            # Colisiones
            jugador_rect = pygame.Rect(jugador_x + offset_x_colision, jugador_y + offset_y_colision, ancho_rect_jugador, alto_rect_jugador)
            colision = False
            for obs in obstaculos:
                obs_rect = pygame.Rect(obs[1], obs[2], obs[0].get_width(), obs[0].get_height())
                if jugador_rect.colliderect(obs_rect):
                    colision = True
                    break

            if colision:
                en_game_over = True

            dibujar()
        else:
            pantalla_game_over()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()