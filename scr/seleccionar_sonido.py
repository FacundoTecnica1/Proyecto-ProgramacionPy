import pygame
import sys

class SelectorSonido:
    def __init__(self, pantalla, ancho, alto, volumen_musica=0.5, volumen_sfx=0.5):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.volumen_musica = volumen_musica
        self.volumen_sfx = volumen_sfx
        self.seleccion = 0  # 0 = música, 1 = SFX

        # Animación suave
        self.volumen_animado = [volumen_musica, volumen_sfx]

        # Colores y fuentes
        self.color_fondo = (20, 20, 30)
        self.color_barra_base = (70, 70, 100)
        self.color_barra_relleno = (50, 200, 255)
        self.color_resaltado = (255, 180, 50)
        self.color_texto = (255, 255, 255)
        self.color_titulo = (255, 220, 100)
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_texto = pygame.font.Font(None, 50)
        self.fuente_porcentaje = pygame.font.Font(None, 35)

        # Posición y tamaño de barras
        self.pos_barras = [
            (self.ancho // 2 - 200, self.alto // 2 - 50),
            (self.ancho // 2 - 200, self.alto // 2 + 80)
        ]
        self.tamano_barra = (400, 40)

        # Sonido de prueba
        try:
            self.sonido_prueba = pygame.mixer.Sound("musica/EfectoSonidoSalto.mp3")
        except:
            self.sonido_prueba = None

    def dibujar_barra(self, x, y, ancho, alto, valor, resaltada=False):
        pygame.draw.rect(self.pantalla, self.color_barra_base, (x, y, ancho, alto), border_radius=15)
        relleno_ancho = int(ancho * valor)
        color_relleno = self.color_resaltado if resaltada else self.color_barra_relleno
        pygame.draw.rect(self.pantalla, color_relleno, (x, y, relleno_ancho, alto), border_radius=15)
        porcentaje = int(valor * 100)
        texto_pct = self.fuente_porcentaje.render(f"{porcentaje}%", True, self.color_texto)
        self.pantalla.blit(texto_pct, texto_pct.get_rect(center=(x + ancho + 50, y + alto // 2)))

    def mostrar(self):
        clock = pygame.time.Clock()
        corriendo = True

        while corriendo:
            dt = clock.tick(60) / 1_000

            self.pantalla.fill(self.color_fondo)

            # Título
            titulo = self.fuente_titulo.render("Configuración de Sonido", True, self.color_titulo)
            self.pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 120)))

            # Barras y animación suave
            valores = [self.volumen_musica, self.volumen_sfx]
            for i in range(2):
                if self.volumen_animado[i] < valores[i]:
                    self.volumen_animado[i] = min(self.volumen_animado[i] + dt * 1.5, valores[i])
                elif self.volumen_animado[i] > valores[i]:
                    self.volumen_animado[i] = max(self.volumen_animado[i] - dt * 1.5, valores[i])

            textos = ["🎵 Música", "🔊 Efectos"]
            for i, (texto, valor) in enumerate(zip(textos, self.volumen_animado)):
                text_surf = self.fuente_texto.render(texto, True, self.color_texto)
                self.pantalla.blit(text_surf, text_surf.get_rect(midleft=(self.pos_barras[i][0], self.pos_barras[i][1] - 10)))
                self.dibujar_barra(self.pos_barras[i][0], self.pos_barras[i][1] + 20, self.tamano_barra[0], self.tamano_barra[1], valor, resaltada=(self.seleccion == i))

        
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        corriendo = False
                    elif event.key == pygame.K_UP:
                        self.seleccion = (self.seleccion - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        self.seleccion = (self.seleccion + 1) % 2
                    elif event.key == pygame.K_LEFT:
                        if self.seleccion == 0:
                            self.volumen_musica = max(0, self.volumen_musica - 0.05)
                        else:
                            self.volumen_sfx = max(0, self.volumen_sfx - 0.05)
                    elif event.key == pygame.K_RIGHT:
                        if self.seleccion == 0:
                            self.volumen_musica = min(1, self.volumen_musica + 0.05)
                        else:
                            self.volumen_sfx = min(1, self.volumen_sfx + 0.05)

            # Aplicar música y SFX
            pygame.mixer.music.set_volume(self.volumen_musica)
            if self.sonido_prueba:
                self.sonido_prueba.set_volume(self.volumen_sfx)

            pygame.display.flip()

        return self.volumen_musica, self.volumen_sfx
