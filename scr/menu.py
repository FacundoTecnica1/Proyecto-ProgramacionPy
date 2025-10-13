import pygame
import sys

class Menu:
    def __init__(self, pantalla, ancho, alto, record_actual):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.record_actual = record_actual
        self.opciones = ["Jugar", "Salir"]
        self.opcion_seleccionada = 0
        self.color_titulo = (255, 220, 100)
        self.color_normal = (180, 180, 180)
        self.color_hover = (255, 255, 255)
        self.color_sombra = (0, 0, 0)
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opcion = pygame.font.Font(None, 60)

    def dibujar_texto(self, texto, fuente, color, x, y, centrado=True, sombra=False):
        if sombra:
            sombra_surface = fuente.render(texto, True, self.color_sombra)
            rect_sombra = sombra_surface.get_rect(center=(x + 3, y + 3))
            self.pantalla.blit(sombra_surface, rect_sombra)
        texto_surface = fuente.render(texto, True, color)
        rect = texto_surface.get_rect(center=(x, y))
        self.pantalla.blit(texto_surface, rect)

    def mostrar(self):
        clock = pygame.time.Clock()
        while True:
            self.pantalla.fill((25, 25, 30))
            self.dibujar_texto("Dino Perro / Gato", self.fuente_titulo, self.color_titulo,
                               self.ancho // 2, 120, sombra=True)

            for i, opcion in enumerate(self.opciones):
                color = self.color_hover if i == self.opcion_seleccionada else self.color_normal
                y = self.alto // 2 + i * 100
                self.dibujar_texto(opcion, self.fuente_opcion, color, self.ancho // 2, y, sombra=True)

            self.dibujar_texto(f"Record: {self.record_actual}", pygame.font.Font(None, 40),
                               (200, 200, 200), self.ancho // 2, self.alto - 60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                    elif event.key == pygame.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                    elif event.key == pygame.K_RETURN:
                        if self.opciones[self.opcion_seleccionada] == "Jugar":
                            return "jugar"
                        elif self.opciones[self.opcion_seleccionada] == "Salir":
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(60)
