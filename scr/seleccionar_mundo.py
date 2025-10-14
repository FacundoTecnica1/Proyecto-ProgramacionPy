import pygame
import sys
import os

class SeleccionMundo:
    def __init__(self, ventana, ancho, alto):
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opciones = pygame.font.Font(None, 60)
        self.clock = pygame.time.Clock()

        self.ruta_img = os.path.join(os.path.dirname(__file__), "..", "img")

        # Fondos
        self.fondo_noche = pygame.image.load(os.path.join(self.ruta_img, "fondo.png")).convert()
        self.fondo_dia = pygame.image.load(os.path.join(self.ruta_img, "fondo2.png")).convert()

        self.fondo_noche = pygame.transform.scale(self.fondo_noche, (ancho, alto))
        self.fondo_dia = pygame.transform.scale(self.fondo_dia, (ancho, alto))

        # Sol y Luna
        self.sol = pygame.transform.scale(pygame.image.load(os.path.join(self.ruta_img, "sol.png")).convert_alpha(), (120, 120))
        self.luna = pygame.transform.scale(pygame.image.load(os.path.join(self.ruta_img, "luna.png")).convert_alpha(), (100, 100))

        # Colores
        self.color_noche = (180, 200, 255)
        self.color_dia = (255, 250, 180)
        self.color_sombra = (0, 0, 0)

    def dibujar_texto(self, texto, fuente, color, x, y, centrado=True):
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect()
        if centrado:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.ventana.blit(superficie, rect)
        return rect

    def mostrar(self):
        seleccion = None
        alpha_fondo = 180
        desplazamiento = 0

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        seleccion = "noche"
                    elif event.key == pygame.K_2:
                        seleccion = "dia"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if boton_noche.collidepoint(mx, my):
                        seleccion = "noche"
                    elif boton_dia.collidepoint(mx, my):
                        seleccion = "dia"

            # Movimiento sutil del fondo
            desplazamiento = (desplazamiento + 0.3) % self.ancho
            self.ventana.blit(self.fondo_dia, (-desplazamiento, 0))
            self.ventana.blit(self.fondo_dia, (self.ancho - desplazamiento, 0))

            # Capa de oscurecimiento
            overlay = pygame.Surface((self.ancho, self.alto))
            overlay.set_alpha(alpha_fondo)
            overlay.fill((0, 0, 0))
            self.ventana.blit(overlay, (0, 0))

            # Título
            self.dibujar_texto("SELECCIONAR MUNDO", self.fuente_titulo, (255, 255, 255), self.ancho // 2, 100)

            # Botones de selección
            mx, my = pygame.mouse.get_pos()
            boton_noche = pygame.Rect(self.ancho // 2 - 300, self.alto // 2 - 100, 250, 180)
            boton_dia = pygame.Rect(self.ancho // 2 + 50, self.alto // 2 - 100, 250, 180)

            pygame.draw.rect(self.ventana, (255, 255, 255, 50), boton_noche, border_radius=20)
            pygame.draw.rect(self.ventana, (255, 255, 255, 50), boton_dia, border_radius=20)

            if boton_noche.collidepoint(mx, my):
                pygame.draw.rect(self.ventana, (150, 180, 255), boton_noche, 5, border_radius=20)
            else:
                pygame.draw.rect(self.ventana, (100, 100, 150), boton_noche, 3, border_radius=20)

            if boton_dia.collidepoint(mx, my):
                pygame.draw.rect(self.ventana, (255, 230, 100), boton_dia, 5, border_radius=20)
            else:
                pygame.draw.rect(self.ventana, (150, 150, 100), boton_dia, 3, border_radius=20)

            # Iconos
            self.ventana.blit(self.luna, (boton_noche.centerx - 50, boton_noche.top + 20))
            self.ventana.blit(self.sol, (boton_dia.centerx - 60, boton_dia.top + 10))

            # Textos
            self.dibujar_texto("MUNDO NOCHE", self.fuente_opciones, self.color_noche, boton_noche.centerx, boton_noche.bottom - 30)
            self.dibujar_texto("MUNDO DÍA", self.fuente_opciones, self.color_dia, boton_dia.centerx, boton_dia.bottom - 30)

            # Instrucciones
            self.dibujar_texto("Presiona 1 o 2, o haz clic para elegir", pygame.font.Font(None, 40), (220, 220, 220),
                               self.ancho // 2, self.alto - 60)

            pygame.display.flip()

            if seleccion:
                return seleccion
