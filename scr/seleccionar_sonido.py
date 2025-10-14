import pygame
import sys
import os

class SelectorSonido:
    def __init__(self, pantalla, ancho, alto, volumen_sfx=0.5):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.volumen_sfx = volumen_sfx

        # Colores y fuentes
        self.color_barra_base = (60, 60, 80)
        self.color_barra_relleno = (0, 200, 255)
        self.color_texto = (245, 245, 245)
        self.color_titulo = (255, 220, 100)
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_texto = pygame.font.Font(None, 55)
        self.fuente_porcentaje = pygame.font.Font(None, 35)

        # Barra
        self.pos_barra = (self.ancho // 2 - 220, self.alto // 2)
        self.tamano_barra = (440, 45)

        # Icono de sonido
        self.icono_sonido = pygame.font.Font(None, 60).render("🔊", True, self.color_texto)

        # Fondo
        try:
            ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
            self.fondo_img = pygame.image.load(ruta_fondo).convert()
            self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))
        except Exception as e:
            print(f"No se pudo cargar fondo.png: {e}")
            self.fondo_img = None

        # Cargar efectos
        try:
            self.salto_sonido = pygame.mixer.Sound(os.path.join("musica", "EfectoSonidoSalto.mp3"))
            self.gameover_sonido = pygame.mixer.Sound(os.path.join("musica", "EfectoSonidoGameOver.mp3"))
        except Exception as e:
            print(f"No se pudieron cargar los efectos de sonido: {e}")
            self.salto_sonido = None
            self.gameover_sonido = None

        # Aplicar volumen inicial
        self.actualizar_volumen()

    def actualizar_volumen(self):
        if self.salto_sonido:
            self.salto_sonido.set_volume(self.volumen_sfx)
        if self.gameover_sonido:
            self.gameover_sonido.set_volume(self.volumen_sfx)

    def dibujar_barra(self, x, y, ancho, alto, valor):
        # Barra base
        pygame.draw.rect(self.pantalla, self.color_barra_base, (x, y, ancho, alto), border_radius=20)

        # Barra rellena con gradiente divertido
        relleno_ancho = int(ancho * valor)
        for i in range(relleno_ancho):
            color = (0, 180 + int(75 * i / ancho), 255)
            pygame.draw.line(self.pantalla, color, (x + i, y), (x + i, y + alto))

        # Porcentaje
        porcentaje = int(valor * 100)
        texto_pct = self.fuente_porcentaje.render(f"{porcentaje}%", True, self.color_texto)
        self.pantalla.blit(texto_pct, texto_pct.get_rect(midleft=(x + ancho + 60, y + alto // 2)))

    def mostrar(self):
        clock = pygame.time.Clock()
        corriendo = True

        while corriendo:
            # Dibujar fondo
            if self.fondo_img:
                self.pantalla.blit(self.fondo_img, (0, 0))
            else:
                self.pantalla.fill((25, 25, 40))

            # Título
            titulo = self.fuente_titulo.render("Volumen Efectos", True, self.color_titulo)
            self.pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 120)))

            # Icono y texto
            self.pantalla.blit(self.icono_sonido, self.icono_sonido.get_rect(midright=(self.pos_barra[0] - 20, self.pos_barra[1])))
            texto = self.fuente_texto.render("Efectos", True, self.color_texto)
            self.pantalla.blit(texto, texto.get_rect(midleft=(self.pos_barra[0], self.pos_barra[1] - 60)))

            # Dibujar barra
            self.dibujar_barra(self.pos_barra[0], self.pos_barra[1], self.tamano_barra[0], self.tamano_barra[1], self.volumen_sfx)

            # Instrucciones
            instrucciones = self.fuente_porcentaje.render("← / → Ajustar | SPACE para probar | ESC salir", True, self.color_texto)
            self.pantalla.blit(instrucciones, instrucciones.get_rect(center=(self.ancho // 2, self.alto - 60)))

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        corriendo = False
                    elif event.key == pygame.K_LEFT:
                        self.volumen_sfx = max(0, self.volumen_sfx - 0.05)
                    elif event.key == pygame.K_RIGHT:
                        self.volumen_sfx = min(1, self.volumen_sfx + 0.05)
                    elif event.key == pygame.K_SPACE:
                        if self.salto_sonido:
                            self.actualizar_volumen()
                            self.salto_sonido.play()

            # Actualizar volumen en tiempo real
            self.actualizar_volumen()

            pygame.display.flip()
            clock.tick(60)

        return self.volumen_sfx
