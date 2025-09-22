import pygame
import serial
import time

# Configurar puerto Arduino (cambiar según tu sistema)
arduino = serial.Serial('COM3', 9600)  # Windows ejemplo: 'COM3'
time.sleep(2)  # Esperar a que Arduino se inicialice

# Configuración de pygame
pygame.init()
ventana = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Sinosaurio")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Jugador simple
jugador = pygame.Rect(50, 200, 40, 40)
salto = False
vel_y = 0

clock = pygame.time.Clock()
running = True

while running:
    ventana.fill(BLANCO)
    pygame.draw.rect(ventana, NEGRO, jugador)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Teclas del juego
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Saltar
                if not salto:
                    vel_y = -10
                    salto = True
                    arduino.write(b'J')
            elif event.key == pygame.K_DOWN:  # Agacharse
                arduino.write(b'G')
            elif event.key == pygame.K_a:     # Atacar
                arduino.write(b'A')

    # Simular gravedad
    if salto:
        vel_y += 0.5
        jugador.y += int(vel_y)
        if jugador.y >= 200:
            jugador.y = 200
            salto = False
            vel_y = 0

    pygame.display.flip()
    clock.tick(60)

    # Leer mensajes de Arduino
    if arduino.in_waiting > 0:
        mensaje = arduino.readline().decode('utf-8').strip()
        print("Arduino:", mensaje)

pygame.quit()
arduino.close()
