import pygame
import sys
import os
import random  # Para brillitos
import serial # <-- MODIFICADO: Importado

# --- RUTAS PARA PYINSTALLER ---
if getattr(sys, 'frozen', False):
    RUTA_BASE = os.path.join(sys._MEIPASS, "img")
else:
    RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

class SeleccionMundo:
    # MODIFICADO: Añadido arduino_serial=None e idioma
    def __init__(self, ventana, ancho, alto, arduino_serial=None, idioma="es"):
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto
        self.arduino_serial = arduino_serial # <-- MODIFICADO
        self.idioma = idioma

        # --- Textos Multi-idioma (MODIFICADO) ---
        self.textos = {
            "es": {
                "titulo": "SELECCIONAR MUNDO",
                "noche": "NOCHE", # MODIFICADO
                "dia": "DÍA",   # MODIFICADO
                "volver": "Volver",
                # MODIFICADO: Separado en dos claves
                "instruccion_cambiar": "Use 'Flecha Izquierda' para cambiar.", 
                "instruccion_seleccionar": "Use 'Flecha Derecha' para seleccionar."
            },
            "en": {
                "titulo": "SELECT WORLD",
                "noche": "NIGHT", # MODIFICADO
                "dia": "DAY",   # MODIFICADO
                "volver": "Back",
                # MODIFICADO: Separado en dos claves
                "instruccion_cambiar": "Use 'Left Arrow' to change.",
                "instruccion_seleccionar": "Use 'Right Arrow' to select."
            }
        }
        self.actualizar_textos() # Asegurar que los textos se carguen correctamente
        
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opciones = pygame.font.Font(None, 60)
        self.fuente_boton = pygame.font.Font(None, 55)
        # MODIFICADO: Fuente para instrucciones más grande
        self.fuente_instruccion = pygame.font.Font(None, 35) 
        self.clock = pygame.time.Clock()

        self.ruta_img = RUTA_BASE

        # Fondos
        self.fondo_noche = pygame.image.load(os.path.join(RUTA_BASE, "fondo.png")).convert()
        self.fondo_dia = pygame.image.load(os.path.join(RUTA_BASE, "fondo2.png")).convert()
        self.fondo_noche = pygame.transform.scale(self.fondo_noche, (ancho, alto))
        self.fondo_dia = pygame.transform.scale(self.fondo_dia, (ancho, alto))

        # Sol y Luna
        self.sol = pygame.transform.scale(pygame.image.load(os.path.join(RUTA_BASE, "sol.png")).convert_alpha(), (120, 120))
        self.luna = pygame.transform.scale(pygame.image.load(os.path.join(RUTA_BASE, "luna.png")).convert_alpha(), (100, 100))

        # Colores vibrantes
        self.color_noche = (150, 200, 255)  # Azul claro vibrante
        self.color_dia = (255, 255, 100)    # Amarillo estándar
        self.color_hover = (255, 100, 50)   # Naranja vibrante
        self.color_sombra = (0, 0, 0, 120)
        self.color_titulo = (255, 255, 100)   # Amarillo estándar
        self.color_fondo_top = (20, 30, 60) # Azul muy oscuro
        self.color_fondo_bottom = (60, 20, 40) # Morado oscuro

        # Estado
        self.seleccion_horizontal = 0  # 0 = noche, 1 = día
        self.en_boton_volver = False

        # Brillitos del selector de mundos
        self.brillitos_mundos = []
        for _ in range(30):
            self.brillitos_mundos.append({
                'x': random.randint(0, ancho),
                'y': random.randint(0, alto),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'color': random.choice([
                    (255, 255, 100),  # Amarillo brillante
                    (100, 255, 255),  # Cyan brillante
                    (255, 100, 255),  # Magenta brillante
                    (100, 255, 100),  # Verde brillante
                    (255, 255, 100),  # Amarillo estándar
                    (200, 100, 255),  # Púrpura brillante
                ]),
                'size': random.randint(1, 3),
                'vida': random.randint(70, 200),
                'vida_max': random.randint(70, 200)
            })

    def dibujar_fondo_colorido(self):
        """Dibuja un fondo degradado colorido estático"""
        # Degradado vertical vibrante
        for y in range(self.alto):
            # Interpolación entre color superior e inferior
            factor = y / self.alto
            r = int(self.color_fondo_top[0] * (1 - factor) + self.color_fondo_bottom[0] * factor)
            g = int(self.color_fondo_top[1] * (1 - factor) + self.color_fondo_bottom[1] * factor)
            b = int(self.color_fondo_top[2] * (1 - factor) + self.color_fondo_bottom[2] * factor)
            
            color = (r, g, b)
            pygame.draw.line(self.ventana, color, (0, y), (self.ancho, y))
        
        # Añadir estrellas coloridas estáticas
        estrellas_positions = [
            (70, 100), (300, 50), (500, 160), (700, 80),
            (100, 350), (450, 300), (650, 400), (150, 250),
            (550, 450), (350, 140), (750, 250), (20, 200)
        ]
        
        colores_estrellas = [
            (255, 255, 150), (150, 255, 255), (255, 150, 255),
            (150, 255, 150), (255, 200, 150), (200, 150, 255)
        ]
        
        for i, pos in enumerate(estrellas_positions):
            if pos[0] < self.ancho and pos[1] < self.alto:
                color = colores_estrellas[i % len(colores_estrellas)]
                pygame.draw.circle(self.ventana, color, pos, 3)

    def dibujar_opcion_mundo(self, mundo, x, y, seleccionado=False):
        """Dibuja una opción de mundo con colores vibrantes"""
        ancho_card, alto_card = 280, 200
        rect = pygame.Rect(x - ancho_card // 2, y - alto_card // 2, ancho_card, alto_card)
        
        # Colores según el mundo y selección
        if mundo == "noche":
            if seleccionado:
                color_fondo = (40, 60, 120)    # Azul oscuro vibrante
                color_borde = (150, 200, 255)  # Azul claro
            else:
                color_fondo = (20, 30, 60)     # Azul muy oscuro
                color_borde = (100, 150, 200)  # Azul medio
            imagen = self.luna
        else:  # día
            if seleccionado:
                color_fondo = (120, 80, 20)    # Naranja oscuro vibrante
                color_borde = (255, 255, 100)  # Amarillo estándar
            else:
                color_fondo = (60, 40, 10)     # Marrón oscuro
                color_borde = (200, 150, 80)   # Marrón claro
            imagen = self.sol
        
        # Sin sombra - directamente fondo y borde
        pygame.draw.rect(self.ventana, color_fondo, rect, border_radius=25)
        pygame.draw.rect(self.ventana, color_borde, rect, 4, border_radius=25)
        
        # Imagen del mundo
        img_rect = imagen.get_rect(center=(x, y - 20))
        self.ventana.blit(imagen, img_rect)
        
        # Texto colorido
        texto = self.txt["noche"] if mundo == "noche" else self.txt["dia"]
        color_texto = self.color_noche if mundo == "noche" else self.color_dia
        if seleccionado:
            color_texto = (255, 255, 255)  # Blanco para seleccionado
        
        self.dibujar_texto(texto, self.fuente_opciones, color_texto, x, y + 60)
        
        return rect

    # ------------------------------------------------------------
    def actualizar_textos(self):
        """Actualiza los textos según el idioma actual"""
        self.txt = self.textos[self.idioma]

    # ------------------------------------------------------------
    def dibujar_texto(self, texto, fuente, color, x, y, centrado=True, sombra_color=(0,0,0)):
        # Sombra
        sombra_surf = fuente.render(texto, True, sombra_color)
        sombra_rect = sombra_surf.get_rect(center=(x + 2, y + 2)) if centrado else sombra_surf.get_rect(topleft=(x + 2, y + 2))
        self.ventana.blit(sombra_surf, sombra_rect)
        
        # Texto
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

    def actualizar_brillitos(self):
        """Actualiza los brillitos del selector de mundos"""
        for brillito in self.brillitos_mundos:
            # Actualizar posición
            brillito['x'] += brillito['vx']
            brillito['y'] += brillito['vy']
            
            # Rebotar en los bordes
            if brillito['x'] <= 0 or brillito['x'] >= self.ancho:
                brillito['vx'] *= -1
            if brillito['y'] <= 0 or brillito['y'] >= self.alto:
                brillito['vy'] *= -1
            
            # Actualizar vida
            brillito['vida'] -= 1
            if brillito['vida'] <= 0:
                # Reiniciar brillito
                brillito['x'] = random.randint(0, self.ancho)
                brillito['y'] = random.randint(0, self.alto)
                brillito['vida'] = brillito['vida_max']

    def dibujar_brillitos(self):
        """Dibuja los brillitos del selector de mundos"""
        for brillito in self.brillitos_mundos:
            # Calcular alpha basado en la vida
            alpha = int(255 * (brillito['vida'] / brillito['vida_max']))
            
            # Crear superficie con alpha
            tamano = brillito['size'] * 2
            surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
            
            # Dibujar círculo principal
            pygame.draw.circle(surf, brillito['color'], (tamano//2, tamano//2), brillito['size'])
            
            # Efecto de brillo adicional
            color_brillo = tuple(min(255, c + 50) for c in brillito['color'])
            pygame.draw.circle(surf, color_brillo, (tamano//2, tamano//2), max(1, brillito['size']//2))
            
            # Aplicar alpha
            surf.set_alpha(alpha)
            
            self.ventana.blit(surf, (int(brillito['x']) - tamano//2, int(brillito['y']) - tamano//2))

    # ------------------------------------------------------------
    def mostrar(self):
        desplazamiento = 0
        while True:
            self.clock.tick(60)

            # Fondo colorido vibrante
            self.dibujar_fondo_colorido()
            
            # Actualizar y dibujar brillitos
            self.actualizar_brillitos()
            self.dibujar_brillitos()

            # Título dorado con sombra
            self.dibujar_texto(self.txt["titulo"], self.fuente_titulo, self.color_titulo, self.ancho // 2, 100)

            # Posiciones para las opciones de mundo
            centro_y = self.alto // 2
            x_noche = self.ancho // 2 - 200
            x_dia = self.ancho // 2 + 200

            # Dibujar opciones de mundo coloridas
            if not self.en_boton_volver:
                self.dibujar_opcion_mundo("noche", x_noche, centro_y, 
                                        seleccionado=(self.seleccion_horizontal == 0))
                self.dibujar_opcion_mundo("dia", x_dia, centro_y, 
                                        seleccionado=(self.seleccion_horizontal == 1))
            else:
                self.dibujar_opcion_mundo("noche", x_noche, centro_y, seleccionado=False)
                self.dibujar_opcion_mundo("dia", x_dia, centro_y, seleccionado=False)

            # ------------------------------------
            # ⬇️ DIBUJAR INSTRUCCIONES COLORIDAS (MODIFICADO) ⬇️
            # ------------------------------------
            color_inst = (255, 200, 150)  # Naranja suave vibrante
            y_instruccion_1 = centro_y + 150
            y_instruccion_2 = y_instruccion_1 + 40 # Espacio vertical para la segunda línea

            self.dibujar_texto(self.txt["instruccion_cambiar"], 
                               self.fuente_instruccion, 
                               color_inst,
                               self.ancho // 2, 
                               y_instruccion_1)
            
            self.dibujar_texto(self.txt["instruccion_seleccionar"], 
                               self.fuente_instruccion, 
                               color_inst,
                               self.ancho // 2, 
                               y_instruccion_2)
            # ------------------------------------
            # ⬆️ FIN INSTRUCCIONES ⬆️
            # ------------------------------------

            # Botón Volver colorido
            rect_volver = pygame.Rect(0, 0, 250, 70)
            rect_volver.center = (self.ancho // 2, self.alto - 100)
            
            if self.en_boton_volver:
                color_btn = (100, 50, 150)    # Morado vibrante
                color_borde = (255, 100, 255) # Magenta
                color_texto = (255, 255, 255)
            else:
                color_btn = (50, 80, 120)     # Azul oscuro
                color_borde = (100, 150, 255) # Azul claro
                color_texto = (200, 200, 255)
            
            # Botón sin sombra
            pygame.draw.rect(self.ventana, color_btn, rect_volver, border_radius=20)
            pygame.draw.rect(self.ventana, color_borde, rect_volver, 3, border_radius=20)
            
            # Texto
            self.dibujar_texto(self.txt["volver"], self.fuente_boton, color_texto,
                              rect_volver.centerx, rect_volver.centery)

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


            # Eventos (MODIFICADOS PARA ARDUINO)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.arduino_serial and self.arduino_serial.is_open:
                        self.arduino_serial.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # D5
                        if self.en_boton_volver:
                            return "volver" # K_LEFT (D5) en Volver = Volver
                        else:
                            self.seleccion_horizontal = (self.seleccion_horizontal - 1) % 2

                    elif event.key == pygame.K_RIGHT: # D3
                        if self.en_boton_volver:
                            return "volver" # K_RIGHT (D3) en Volver = Volver
                        else:
                            # K_RIGHT (D3) es CONFIRMAR
                            return "noche" if self.seleccion_horizontal == 0 else "dia"

                    elif event.key == pygame.K_DOWN: # D4
                        self.en_boton_volver = True

                    elif event.key == pygame.K_UP: # D2
                        self.en_boton_volver = False
                        
                    elif event.key == pygame.K_RETURN: # Mantener Enter
                        if self.en_boton_volver:
                            return "volver"
                        else:
                            return "noche" if self.seleccion_horizontal == 0 else "dia"

                    elif event.key == pygame.K_ESCAPE: # Mantener Escape
                        return "volver"

            pygame.display.flip()