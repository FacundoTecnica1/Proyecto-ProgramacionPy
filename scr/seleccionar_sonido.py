import pygame
import sys
import os
import serial # <-- MODIFICADO: Importado

class SelectorSonido:
    # MODIFICADO: Añadido arduino_serial=None
    def __init__(self, pantalla, ancho, alto, volumen_sfx=0.5, arduino_serial=None):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.volumen_sfx = volumen_sfx
        self.arduino_serial = arduino_serial # <-- MODIFICADO

        self.en_volumen = True  # True: ajustar volumen / False: botón volver

        # --- COLORES ---
        self.color_panel = (0, 0, 0, 200)
        self.color_barra_fondo = (40, 40, 40)
        self.color_barra_relleno = (180, 180, 180)
        self.color_texto = (230, 230, 230)
        self.color_titulo = (255, 255, 255) # Cambiado a blanco
        self.color_boton = (50, 50, 50)
        self.color_boton_sel = (100, 100, 100)
        self.color_borde_panel = (100, 100, 100)
        self.color_barra_borde_sel = (255, 230, 150)

        # --- FUENTES ---
        self.fuente_titulo = pygame.font.Font(None, 100)
        self.fuente_texto = pygame.font.Font(None, 55)
        self.fuente_porcentaje = pygame.font.Font(None, 40)
        self.fuente_boton = pygame.font.Font(None, 50)

        # --- FONDO ---
        try:
            ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
            self.fondo_img = pygame.image.load(ruta_fondo).convert()
            self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))
        except Exception as e:
            print(f"No se pudo cargar fondo.png: {e}")
            self.fondo_img = None

        # --- SONIDOS ---
        try:
            self.salto_sonido = pygame.mixer.Sound(os.path.join("musica", "EfectoSonidoSalto.mp3"))
            self.gameover_sonido = pygame.mixer.Sound(os.path.join("musica", "EfectoSonidoGameOver.mp3"))
        except Exception as e:
            print(f"No se pudieron cargar efectos: {e}")
            self.salto_sonido = None
            self.gameover_sonido = None

        self.actualizar_volumen()

    def actualizar_volumen(self):
        if self.salto_sonido:
            self.salto_sonido.set_volume(self.volumen_sfx)
        if self.gameover_sonido:
            self.gameover_sonido.set_volume(self.volumen_sfx)

    def dibujar_barra(self, x, y, ancho, alto, valor, seleccionado=False):
        barra_rect = pygame.Rect(x, y, ancho, alto)
        
        pygame.draw.rect(self.pantalla, self.color_barra_fondo, barra_rect, border_radius=20)
        relleno_ancho = int(ancho * valor)
        pygame.draw.rect(self.pantalla, self.color_barra_relleno, (x, y, relleno_ancho, alto), border_radius=20)
        
        if seleccionado:
            pygame.draw.rect(self.pantalla, self.color_barra_borde_sel, barra_rect, 4, border_radius=20)

        porcentaje = int(valor * 100)
        texto_pct = self.fuente_porcentaje.render(f"{porcentaje}%", True, self.color_texto)
        self.pantalla.blit(texto_pct, texto_pct.get_rect(midleft=(x + ancho + 20, y + alto // 2)))

    def mostrar(self):
        clock = pygame.time.Clock()
        corriendo = True

        # Panel más ancho, con bordes redondeados
        panel_width = self.ancho // 1.2
        panel_height = self.alto // 2.2
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_rect = panel_surface.get_rect(center=(self.ancho // 2, self.alto // 2 + 20))

        while corriendo:
            # Fondo
            if self.fondo_img:
                self.pantalla.blit(self.fondo_img, (0, 0))
            else:
                self.pantalla.fill((20, 20, 25))
                
            # Capa oscura
            overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.pantalla.blit(overlay, (0,0))

            # Título (fuera del panel)
            titulo = self.fuente_titulo.render("Volumen Efectos", True, self.color_titulo)
            self.pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, panel_rect.top - 60)))

            # Panel negro con bordes redondeados y borde gris
            panel_surface.fill((0, 0, 0, 0))
            pygame.draw.rect(panel_surface, self.color_panel, (0, 0, panel_width, panel_height), border_radius=30)
            pygame.draw.rect(panel_surface, self.color_borde_panel, (0, 0, panel_width, panel_height), 3, border_radius=30)
            self.pantalla.blit(panel_surface, panel_rect)

            # Texto “Efectos”
            texto = self.fuente_texto.render("Efectos", True, self.color_texto)
            self.pantalla.blit(texto, texto.get_rect(midright=(self.ancho // 2 - 250, panel_rect.centery - 10)))

            # Barra dentro del panel
            self.dibujar_barra(self.ancho // 2 - 180, panel_rect.centery - 22, 360, 45, self.volumen_sfx, seleccionado=self.en_volumen)

            # Botón “Volver”
            boton_rect = pygame.Rect(self.ancho//2 - 100, panel_rect.bottom - 100, 200, 60)
            color_boton = self.color_boton_sel if not self.en_volumen else self.color_boton
            pygame.draw.rect(self.pantalla, color_boton, boton_rect, border_radius=15)
            
            color_borde_boton = (150, 150, 150)
            if not self.en_volumen:
                color_borde_boton = self.color_barra_borde_sel
            pygame.draw.rect(self.pantalla, color_borde_boton, boton_rect, 3, border_radius=15)
            
            txt_boton = self.fuente_boton.render("Volver", True, self.color_texto)
            self.pantalla.blit(txt_boton, txt_boton.get_rect(center=boton_rect.center))

            # ----------------------------------------------------
            # ⬇️ BLOQUE DE LECTURA SERIAL (AÑADIDO) ⬇️
            # ----------------------------------------------------
            if self.arduino_serial is not None and self.arduino_serial.is_open:
                try:
                    while self.arduino_serial.in_waiting > 0:
                        linea = self.arduino_serial.readline().decode('utf-8').strip()
                        
                        evento_tipo = None
                        evento_key = None

                        if linea == "UP_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_UP
                        elif linea == "DOWN_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_DOWN
                        elif linea == "LEFT_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_LEFT
                        elif linea == "RIGHT_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_RIGHT

                        if evento_tipo is not None:
                            evento_post = pygame.event.Event(evento_tipo, key=evento_key)
                            pygame.event.post(evento_post)
                            
                except Exception as e:
                    print(f"[ERROR SERIAL] Lectura/Conexión fallida: {e}")
                    try:
                        self.arduino_serial.close()
                    except Exception:
                        pass
                    self.arduino_serial = None
            # ⬆️ FIN BLOQUE DE LECTURA SERIAL ⬆️
            # ----------------------------------------------------


            # Eventos (MODIFICADOS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.arduino_serial and self.arduino_serial.is_open:
                        self.arduino_serial.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.en_volumen:
                        if event.key == pygame.K_LEFT:
                            self.volumen_sfx = max(0, self.volumen_sfx - 0.05)
                        elif event.key == pygame.K_RIGHT:
                            self.volumen_sfx = min(1, self.volumen_sfx + 0.05)
                        elif event.key == pygame.K_DOWN:
                            self.en_volumen = False
                        elif event.key == pygame.K_SPACE: # Para probar el sonido
                            if self.salto_sonido:
                                self.actualizar_volumen()
                                self.salto_sonido.play()
                    else: # Estamos en "Volver"
                        if event.key == pygame.K_UP:
                            self.en_volumen = True
                        elif event.key == pygame.K_RIGHT: # Seleccionar Volver
                            corriendo = False
                        elif event.key == pygame.K_LEFT: # Ir Atrás
                            corriendo = False
                    
                    if event.key == pygame.K_ESCAPE: # Salir con Escape
                        corriendo = False


            self.actualizar_volumen()
            pygame.display.flip()
            clock.tick(60)

        return self.volumen_sfx