import pygame
import sys
import os

class SeleccionPersonaje:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto

        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 95)
        self.fuente_boton = pygame.font.Font(None, 50)
        self.fuente_texto = pygame.font.Font(None, 42)

        # Colores
        self.color_titulo = (255, 255, 255)
        self.color_boton_activo = (0, 200, 0)
        self.color_boton_inactivo = (200, 0, 0)
        self.color_texto = (255, 255, 255)
        self.color_panel = (0, 0, 0, 120)
        self.color_regresar = (40, 40, 40)  # gris oscuro

        # Cargar fondo e imágenes
        ruta_base = os.path.join(os.path.dirname(__file__), "..", "img")
        self.fondo = pygame.image.load(os.path.join(ruta_base, "fondo.png")).convert()
        self.fondo = pygame.transform.scale(self.fondo, (ancho, alto))

        self.img_perro = pygame.image.load(os.path.join(ruta_base, "Elegir_Personaje_Perro.png")).convert_alpha()
        self.img_gato = pygame.image.load(os.path.join(ruta_base, "Elegir_Personaje_Gato.png")).convert_alpha()

        # Tamaño más natural y equilibrado
        tamaño = (240, 240)
        self.img_perro = pygame.transform.smoothscale(self.img_perro, tamaño)
        self.img_gato = pygame.transform.smoothscale(self.img_gato, tamaño)

        # Más juntos y centrados
        espacio_lateral = 220
        offset_y = 30  # ajusta altura general del bloque
        self.pos_perro = (
            self.ancho // 2 - espacio_lateral - tamaño[0] // 2,
            self.alto // 2 - tamaño[1] // 2 + offset_y,
        )
        self.pos_gato = (
            self.ancho // 2 + espacio_lateral - tamaño[0] // 2,
            self.alto // 2 - tamaño[1] // 2 + offset_y,
        )

        # Estado
        self.equipado = "perro"
        self.rect_regresar = None

    # ===========================================================
    def mostrar(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if self.rect_btn_perro.collidepoint(x, y):
                        self.equipado = "perro"
                    elif self.rect_btn_gato.collidepoint(x, y):
                        self.equipado = "gato"
                    elif self.rect_regresar.collidepoint(x, y):
                        return self.equipado

            self.pantalla.blit(self.fondo, (0, 0))

            self._dibujar_titulo()
            self._dibujar_personaje(self.img_perro, self.pos_perro, "PERRO", self.equipado == "perro")
            self._dibujar_personaje(self.img_gato, self.pos_gato, "GATO", self.equipado == "gato")
            self._dibujar_regresar()

            pygame.display.flip()
            clock.tick(60)

    # ===========================================================
    def _dibujar_titulo(self):
        texto = self.fuente_titulo.render("ELEGÍ TU PERSONAJE", True, self.color_titulo)
        rect = texto.get_rect(center=(self.ancho // 2, 70))  # más arriba
        self.pantalla.blit(texto, rect)

    # ===========================================================
    def _dibujar_personaje(self, imagen, pos, nombre, activo):
        ancho_panel = imagen.get_width() + 60
        alto_panel = imagen.get_height() + 170

        panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 100))
        pygame.draw.rect(panel, (255, 255, 255, 60), panel.get_rect(), border_radius=25)
        rect_panel = panel.get_rect(center=(pos[0] + imagen.get_width() // 2, pos[1] + imagen.get_height() // 2 + 55))
        self.pantalla.blit(panel, rect_panel)

        # Imagen
        self.pantalla.blit(imagen, pos)

        # Nombre debajo de la imagen
        texto_nombre = self.fuente_texto.render(nombre, True, self.color_texto)
        rect_nombre = texto_nombre.get_rect(center=(pos[0] + imagen.get_width() // 2, pos[1] + imagen.get_height() + 35))
        self.pantalla.blit(texto_nombre, rect_nombre)

        # Botón
        texto_boton = "DESEQUIPAR" if activo else "EQUIPAR"
        color = self.color_boton_inactivo if activo else self.color_boton_activo
        boton_surface = pygame.Surface((200, 50))
        boton_surface.fill(color)
        texto_render = self.fuente_boton.render(texto_boton, True, self.color_texto)
        rect_texto = texto_render.get_rect(center=(100, 25))
        boton_surface.blit(texto_render, rect_texto)
        rect_boton = boton_surface.get_rect(center=(pos[0] + imagen.get_width() // 2, pos[1] + imagen.get_height() + 95))
        self.pantalla.blit(boton_surface, rect_boton)

        if nombre == "PERRO":
            self.rect_btn_perro = rect_boton
        else:
            self.rect_btn_gato = rect_boton

    # ===========================================================
    def _dibujar_regresar(self):
        texto = self.fuente_boton.render("REGRESAR", True, (255, 255, 255))
        boton_surface = pygame.Surface((260, 55))
        boton_surface.fill(self.color_regresar)
        rect_texto = texto.get_rect(center=(130, 27))
        boton_surface.blit(texto, rect_texto)
        rect_boton = boton_surface.get_rect(center=(self.ancho // 2, self.alto - 40))  # abajo de todo
        self.pantalla.blit(boton_surface, rect_boton)
        self.rect_regresar = rect_boton
