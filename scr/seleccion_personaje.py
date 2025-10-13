import pygame
import sys
import os

class SeleccionPersonaje:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto

        self.color_titulo = (255, 220, 100)
        self.color_normal = (180, 180, 180)
        self.color_hover = (255, 255, 255)
        self.color_sombra = (0, 0, 0)

        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opcion = pygame.font.Font(None, 60)

        ruta_base = os.path.join(os.path.dirname(__file__), "..", "img")
        self.img_perro = pygame.transform.scale(
            pygame.image.load(os.path.join(ruta_base, "perro_run1.png")).convert_alpha(), (150, 150)
        )
        self.img_gato = pygame.transform.scale(
            pygame.image.load(os.path.join(ruta_base, "gato_run1.png")).convert_alpha(), (150, 150)
        )

        self.opciones = ["Perro", "Gato"]
        self.opcion_sel = 0

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
            self.dibujar_texto("Selecciona tu personaje", self.fuente_titulo, self.color_titulo,
                               self.ancho // 2, 100, sombra=True)

            for i, opcion in enumerate(self.opciones):
                color = self.color_hover if i == self.opcion_sel else self.color_normal
                y = self.alto // 2 + i * 150
                self.dibujar_texto(opcion, self.fuente_opcion, color, self.ancho // 2, y + 90, sombra=True)
                img = self.img_perro if opcion == "Perro" else self.img_gato
                rect = img.get_rect(center=(self.ancho // 2, y))
                self.pantalla.blit(img, rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.opcion_sel = (self.opcion_sel - 1) % len(self.opciones)
                    elif event.key == pygame.K_DOWN:
                        self.opcion_sel = (self.opcion_sel + 1) % len(self.opciones)
                    elif event.key == pygame.K_RETURN:
                        return self.opciones[self.opcion_sel].lower()

            pygame.display.flip()
            clock.tick(60)
