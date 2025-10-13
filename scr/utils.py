import pygame

def mostrar_texto(texto, x, y, color, pantalla, tam=30, centrado=False):
    fuente = pygame.font.Font(None, tam)
    superficie = fuente.render(str(texto), True, color)
    rect = superficie.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    pantalla.blit(superficie, rect)
