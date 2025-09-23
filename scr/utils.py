import pygame

# Colores
BLANCO = (255, 255, 255)

def mostrar_texto(texto, x, y, color, superficie, tamaño=28, centrado=False):
    fuente = pygame.font.SysFont("Arial", tamaño)
    render = fuente.render(texto, True, color)
    if centrado:
        render_rect = render.get_rect(center=(x, y))
        superficie.blit(render, render_rect)
    else:
        superficie.blit(render, (x, y))