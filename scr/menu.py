import pygame
import sys
import math
import os
from seleccion_personaje import SeleccionPersonaje

class Menu:
    def __init__(self, pantalla, ancho, alto, record_actual):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.record_actual = record_actual

        self.color_titulo = (255, 200, 0)
        self.color_boton_normal = (180, 180, 180)
        self.color_boton_hover = (255, 255, 255)
        self.color_sombra = (0, 0, 0)

        self.fuente_titulo = pygame.font.Font(None, 120)
        self.fuente_boton = pygame.font.Font(None, 60)
        self.fuente_record = pygame.font.Font(None, 45)

        self.opciones = ["Jugar", "Ver récord", "Elegir personaje", "Salir"]
        self.opcion_seleccionada = 0

        ruta_base = os.path.join(os.path.dirname(__file__), "..", "img")
        self.fondo = pygame.image.load(os.path.join(ruta_base, "fondo.png")).convert()
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.alto))

        self.personaje = "perro"

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
        anim_tiempo = 0

        while True:
            anim_tiempo += 1
            self.pantalla.blit(self.fondo, (0, 0))

            escala = 1 + 0.02 * math.sin(anim_tiempo * 0.05)
            titulo_surface = self.fuente_titulo.render("Dino Perro", True, self.color_titulo)
            titulo_surface = pygame.transform.rotozoom(titulo_surface, 0, escala)
            rect_titulo = titulo_surface.get_rect(center=(self.ancho // 2, self.alto // 3))
            self.pantalla.blit(titulo_surface, rect_titulo)

            for i, opcion in enumerate(self.opciones):
                color = self.color_boton_hover if i == self.opcion_seleccionada else self.color_boton_normal
                y = self.alto // 2 + i * 80
                self.dibujar_texto(opcion, self.fuente_boton, color, self.ancho // 2, y, sombra=True)

            self.dibujar_texto(f"Récord actual: {self.record_actual}",
                               self.fuente_record, (200, 200, 200),
                               self.ancho // 2, self.alto - 80, sombra=True)

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
                        seleccion = self.opciones[self.opcion_seleccionada]
                        if seleccion == "Jugar":
                            return "jugar", self.personaje
                        elif seleccion == "Ver récord":
                            return "record", self.personaje
                        elif seleccion == "Salir":
                            return "salir", self.personaje
                        elif seleccion == "Elegir personaje":
                            seleccionador = SeleccionPersonaje(self.pantalla, self.ancho, self.alto)
                            elegido = seleccionador.mostrar()
                            if elegido:
                                self.personaje = elegido

            pygame.display.flip()
            clock.tick(60)
