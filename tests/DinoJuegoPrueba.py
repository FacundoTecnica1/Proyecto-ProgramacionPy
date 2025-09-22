import pygame
import serial
import sys

# =====================
# Configuración inicial
# =====================
pygame.init()
ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino con Arduino")
clock = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 200, 0)

# Dino
dino_x = 50
dino_y = ALTO - 80
dino_width = 40
dino_height = 60
vel_salto = 0
en_suelo = True
agachado = False

# Serial (ajustar puerto según tu PC)
arduino = serial.Serial('COM3', 9600)

# =====================
# Funciones del Dino
# =====================
def saltar():
    global vel_salto, en_suelo
    if en_suelo:
        vel_salto = -15
        en_suelo = False

def agachar(estado):
    global agachado, dino_height
    agachado = estado
    if agachado:
        dino_height = 30
    else:
        dino_height = 60

def reiniciar():
    global dino_y, vel_salto, en_suelo
    dino_y = ALTO - 80
    vel_salto = 0
    en_suelo = True

# =====================
# Bucle principal
# =====================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Leer datos de Arduino
    if arduino.in_waiting > 0:
        accion = arduino.readline().decode().strip()
        print("Acción:", accion)

        if accion == "SALTO":
            saltar()
        elif accion == "AGACHAR":
            agachar(True)
        elif accion == "REINICIO":
            reiniciar()

    # Física del salto
    if not en_suelo:
        dino_y += vel_salto
        vel_salto += 1
        if dino_y >= ALTO - 80:
            dino_y = ALTO - 80
            en_suelo = True

    # Si no mantiene botón agachado → vuelve normal
    keys = pygame.key.get_pressed()  # fallback con teclado
    if not keys[pygame.K_DOWN]:
        agachar(False)

    # Dibujar
    ventana.fill(BLANCO)
    pygame.draw.rect(ventana, VERDE, (dino_x, dino_y, dino_width, dino_height))
    pygame.display.flip()
    clock.tick(60)
