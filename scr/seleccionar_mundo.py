import pygame
import sys
import os
import serial # <-- MODIFICADO: Importado

class SeleccionMundo:
    # MODIFICADO: Añadido arduino_serial=None
    def __init__(self, ventana, ancho, alto, arduino_serial=None):
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto
        self.arduino_serial = arduino_serial # <-- MODIFICADO
        
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opciones = pygame.font.Font(None, 60)
        self.fuente_boton = pygame.font.Font(None, 55)
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
        self.color_hover = (255, 230, 150)
        self.color_sombra = (0, 0, 0, 120)

        # Estado
        self.seleccion_horizontal = 0  # 0 = noche, 1 = día
        self.en_boton_volver = False

    # ------------------------------------------------------------
    def dibujar_texto(self, texto, fuente, color, x, y, centrado=True):
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(x, y)) if centrado else superficie.get_rect(topleft=(x, y))
        self.ventana.blit(superficie, rect)
        return rect

    # ------------------------------------------------------------
    def dibujar_boton(self, texto, x, y, ancho, alto, seleccionado=False):
        rect = pygame.Rect(x - ancho // 2, y - alto // 2, ancho, alto)
        color = self.color_hover if seleccionado else (50, 50, 50)
        
        sombra_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, (0, 0, 0, 120), sombra_surf.get_rect(), border_radius=20)
        self.ventana.blit(sombra_surf, rect.move(4, 4))
        
        pygame.draw.rect(self.ventana, color, rect, border_radius=20)
        pygame.draw.rect(self.ventana, (255, 255, 255), rect, 3, border_radius=20)
        texto_surf = self.fuente_boton.render(texto, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.ventana.blit(texto_surf, texto_rect)
        return rect

    # ------------------------------------------------------------
    def mostrar(self):
        desplazamiento = 0
        while True:
            self.clock.tick(60)

            # Fondo en movimiento
            desplazamiento = (desplazamiento + 0.3) % self.ancho
            self.ventana.blit(self.fondo_dia, (-desplazamiento, 0))
            self.ventana.blit(self.fondo_dia, (self.ancho - desplazamiento, 0))

            # Oscurecer capa
            overlay = pygame.Surface((self.ancho, self.alto))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.ventana.blit(overlay, (0, 0))

            # Título
            self.dibujar_texto("SELECCIONAR MUNDO", self.fuente_titulo, (255, 255, 255), self.ancho // 2, 100)

            # Botones de mundos
            boton_noche = pygame.Rect(self.ancho // 2 - 300, self.alto // 2 - 100, 250, 180)
            boton_dia = pygame.Rect(self.ancho // 2 + 50, self.alto // 2 - 100, 250, 180)

            # Resaltado según selección
            if not self.en_boton_volver:
                if self.seleccion_horizontal == 0:
                    pygame.draw.rect(self.ventana, (150, 180, 255), boton_noche, 5, border_radius=20)
                    pygame.draw.rect(self.ventana, (100, 100, 150), boton_dia, 3, border_radius=20)
                else:
                    pygame.draw.rect(self.ventana, (150, 150, 100), boton_noche, 3, border_radius=20)
                    pygame.draw.rect(self.ventana, (255, 230, 100), boton_dia, 5, border_radius=20)
            else:
                pygame.draw.rect(self.ventana, (100, 100, 150), boton_noche, 3, border_radius=20)
                pygame.draw.rect(self.ventana, (150, 150, 100), boton_dia, 3, border_radius=20)

            # Iconos
            self.ventana.blit(self.luna, (boton_noche.centerx - 50, boton_noche.top + 20))
            self.ventana.blit(self.sol, (boton_dia.centerx - 60, boton_dia.top + 10))

            # Textos de mundos
            self.dibujar_texto("MUNDO NOCHE", self.fuente_opciones, self.color_noche, boton_noche.centerx, boton_noche.bottom - 30)
            self.dibujar_texto("MUNDO DÍA", self.fuente_opciones, self.color_dia, boton_dia.centerx, boton_dia.bottom - 30)

            # Botón Volver
            boton_volver = self.dibujar_boton("Volver", self.ancho // 2, self.alto - 100, 250, 70, seleccionado=self.en_boton_volver)

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
                    if event.key == pygame.K_LEFT:
                        if not self.en_boton_volver:
                            self.seleccion_horizontal = (self.seleccion_horizontal - 1) % 2
                        else:
                            return "volver" # K_LEFT en "Volver" = Volver

                    elif event.key == pygame.K_RIGHT:
                        if self.en_boton_volver:
                            # Confirmar volver
                            return "volver"
                        else:
                            # Moverse o Confirmar mundo
                            if self.seleccion_horizontal == 0:
                                self.seleccion_horizontal = 1 # Mover Noche -> Día
                            elif self.seleccion_horizontal == 1:
                                # Confirmar Día
                                return "dia" 

                    elif event.key == pygame.K_DOWN:
                        self.en_boton_volver = True

                    elif event.key == pygame.K_UP:
                        self.en_boton_volver = False
                        
                    elif event.key == pygame.K_RETURN: # Mantener Enter
                        if self.en_boton_volver:
                            return "volver"
                        else:
                            return "noche" if self.seleccion_horizontal == 0 else "dia"

                    elif event.key == pygame.K_ESCAPE: # Mantener Escape
                        return "volver"

            pygame.display.flip()