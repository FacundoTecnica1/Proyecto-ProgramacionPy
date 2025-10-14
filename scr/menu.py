import pygame
import sys
import os
from seleccionar_sonido import SelectorSonido

class Menu:
    def __init__(self, pantalla, ancho, alto, record_actual):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.record_actual = record_actual
        self.opciones = ["Jugar", "Elegir Mundo", "Sonidos", "Salir"]
        self.opcion_seleccionada = 0

        # Colores y fuentes
        self.color_texto = (255, 255, 255)
        self.color_hover = (255, 230, 150)
        self.color_sombra = (0, 0, 0, 120)  # sombra más visible
        self.color_boton = (50, 50, 50)
        self.radio_boton = 20
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opcion = pygame.font.Font(None, 55)
        self.fuente_record = pygame.font.Font(None, 40)

        # Volúmenes
        self.volumen_musica = 0.5
        self.volumen_sfx = 0.5

        # Fondo
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
        self.fondo_img = pygame.image.load(ruta_fondo).convert()
        self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))

        # Botones (rects para detección)
        self.botones_rects = []

    def dibujar_boton(self, texto, x, y, seleccionado=False):
        # --- Rectángulo del botón ---
        ancho_boton, alto_boton = 350, 60  # más largo
        rect = pygame.Rect(0, 0, ancho_boton, alto_boton)
        rect.center = (x, y)

        # --- Sombra ---
        sombra_rect = rect.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        sombra_surf = pygame.Surface((ancho_boton, alto_boton), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, self.color_sombra, sombra_surf.get_rect(), border_radius=self.radio_boton)
        self.pantalla.blit(sombra_surf, sombra_rect.topleft)

        # --- Color del botón ---
        color = self.color_hover if seleccionado else self.color_boton
        pygame.draw.rect(self.pantalla, color, rect, border_radius=self.radio_boton)

        # --- Texto centrado ---
        texto_surf = self.fuente_opcion.render(texto, True, self.color_texto)
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.pantalla.blit(texto_surf, texto_rect)

        return rect

    def mostrar(self):
        clock = pygame.time.Clock()
        while True:
            self.pantalla.blit(self.fondo_img, (0, 0))  # fondo

            # --- Título ---
            titulo_surf = self.fuente_titulo.render("Dino Perro / Gato", True, self.color_texto)
            titulo_rect = titulo_surf.get_rect(center=(self.ancho // 2, 80))
            self.pantalla.blit(titulo_surf, titulo_rect)

            # --- Opciones como botones ---
            self.botones_rects.clear()
            espacio_vertical = 90
            inicio_y = self.alto // 2 - ((len(self.opciones) - 1) * espacio_vertical) // 2 + 100
            for i, opcion in enumerate(self.opciones):
                y = inicio_y + i * espacio_vertical
                rect = self.dibujar_boton(opcion, self.ancho // 2, y,
                                          seleccionado=(i == self.opcion_seleccionada))
                self.botones_rects.append(rect)

            # --- Record ---
            record_surf = self.fuente_record.render(f"Record: {self.record_actual}", True, self.color_texto)
            record_rect = record_surf.get_rect(center=(self.ancho // 2, self.alto - 380))
            self.pantalla.blit(record_surf, record_rect)

            # --- Eventos ---
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
                            return "jugar"
                        elif seleccion == "Elegir Mundo":
                            return "mundo"
                        elif seleccion == "Sonidos":
                            selector = SelectorSonido(self.pantalla, self.ancho, self.alto,
                                                      self.volumen_musica, self.volumen_sfx)
                            self.volumen_musica, self.volumen_sfx = selector.mostrar()
                            pygame.mixer.music.set_volume(self.volumen_musica)
                        elif seleccion == "Salir":
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(60)
