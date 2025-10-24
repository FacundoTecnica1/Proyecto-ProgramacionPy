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
        self.opciones = [
            "Jugar",
            "Elegir Nombre",
            "Elegir Mundo",
            "Sonidos",
            "Ver Rankings",
            "Salir"
        ]
        self.opcion_seleccionada = 0

        # Colores y fuentes
        self.color_texto = (255, 255, 255)
        self.color_hover = (255, 230, 150)
        self.color_sombra = (0, 0, 0, 120)
        self.color_boton = (50, 50, 50)
        self.radio_boton = 20
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opcion = pygame.font.Font(None, 55)
        self.fuente_record = pygame.font.Font(None, 40)

        # Volumen efectos
        self.volumen_sfx = 0.5

        # Fondo
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
        self.fondo_img = pygame.image.load(ruta_fondo).convert()
        self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))

        self.botones_rects = []
        self.nombre_actual = None
        self.id_usuario_actual = None

    def dibujar_boton(self, texto, x, y, seleccionado=False):
        ancho_boton, alto_boton = 350, 60
        rect = pygame.Rect(0, 0, ancho_boton, alto_boton)
        rect.center = (x, y)

        # Sombra del botón
        sombra_rect = rect.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        sombra_surf = pygame.Surface((ancho_boton, alto_boton), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, self.color_sombra, sombra_surf.get_rect(), border_radius=self.radio_boton)
        self.pantalla.blit(sombra_surf, sombra_rect.topleft)

        # Botón principal
        color = self.color_hover if seleccionado else self.color_boton
        pygame.draw.rect(self.pantalla, color, rect, border_radius=self.radio_boton)

        # Texto
        texto_surf = self.fuente_opcion.render(texto, True, self.color_texto)
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.pantalla.blit(texto_surf, texto_rect)

        return rect

    def mostrar(self):
        clock = pygame.time.Clock()
        while True:
            self.pantalla.blit(self.fondo_img, (0, 0))

            # --- Título ---
            titulo_surf = self.fuente_titulo.render("Dino", True, self.color_texto)
            titulo_rect = titulo_surf.get_rect(center=(self.ancho // 2, 100))
            self.pantalla.blit(titulo_surf, titulo_rect)

            # --- Distribución en 2 columnas ---
            self.botones_rects.clear()
            espacio_vertical = 100
            inicio_y = self.alto // 2 - 150

            columna_izq_x = self.ancho // 2 - 200
            columna_der_x = self.ancho // 2 + 200

            for i, opcion in enumerate(self.opciones):
                # Las 3 primeras a la izquierda, las otras 3 a la derecha
                if i < 3:
                    x = columna_izq_x
                    y = inicio_y + i * espacio_vertical
                else:
                    x = columna_der_x
                    y = inicio_y + (i - 3) * espacio_vertical

                rect = self.dibujar_boton(opcion, x, y, seleccionado=(i == self.opcion_seleccionada))
                self.botones_rects.append(rect)

            # Record actual
            record_surf = self.fuente_record.render(f"Record: {self.record_actual}", True, self.color_texto)
            record_rect = record_surf.get_rect(center=(self.ancho // 2, self.alto - 120))
            self.pantalla.blit(record_surf, record_rect)

            # Nombre actual (si existe)
            if self.nombre_actual:
                nombre_surf = self.fuente_record.render(f"Jugador: {self.nombre_actual}", True, self.color_texto)
                nombre_rect = nombre_surf.get_rect(center=(self.ancho // 2, self.alto - 80))
                self.pantalla.blit(nombre_surf, nombre_rect)

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
                        elif seleccion == "Elegir Nombre":
                            from elegir_nombre import ElegirNombre
                            elegir_nombre = ElegirNombre(self.pantalla, self.ancho, self.alto)
                            nombre, id_usuario = elegir_nombre.mostrar()
                            self.nombre_actual = nombre
                            self.id_usuario_actual = id_usuario
                        elif seleccion == "Elegir Mundo":
                            return "mundo"
                        elif seleccion == "Sonidos":
                            selector = SelectorSonido(self.pantalla, self.ancho, self.alto, self.volumen_sfx)
                            self.volumen_sfx = selector.mostrar()
                        elif seleccion == "Ver Rankings":
                            from mostrar_ranking import MostrarRanking
                            pantalla_ranking = MostrarRanking(self.pantalla, self.ancho, self.alto)
                            pantalla_ranking.mostrar()
                        elif seleccion == "Salir":
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(60)
