import pygame
import sys
import os
import random
import serial 


# --- FUNCIÓN PARA CARGAR IMAGEN ---
def cargar_imagen(nombre):
    ruta_base = os.path.join(os.path.dirname(__file__), "..", "img")
    return pygame.image.load(os.path.join(ruta_base, nombre)).convert_alpha()


# --- FUNCIÓN PARA ESCALAR LISTAS DE IMÁGENES ---
def escalar_lista(lista, w, h):
    return [pygame.transform.smoothscale(img, (w, h)) for img in lista]


# --- FUNCIÓN PARA ESCALAR Y CENTRAR EN CUADRADO ---
def escalar_y_cuadrar(img, size):
    """Escala una imagen manteniendo el aspecto y la centra en un lienzo cuadrado."""
    w, h = img.get_size()
    factor = min(size / w, size / h)
    new_w, new_h = int(w * factor), int(h * factor)
    img_escalada = pygame.transform.smoothscale(img, (new_w, new_h))
    lienzo = pygame.Surface((size, size), pygame.SRCALPHA)
    lienzo.blit(img_escalada, ((size - new_w) // 2, (size - new_h) // 2))
    return lienzo


class Polvo:
    """Partícula de polvo que aparece debajo de los personajes"""
    def __init__(self, x, y):
        self.x = x + random.randint(-10, 10)
        self.y = y + random.randint(10, 15)
        self.radio = random.randint(3, 6)
        self.velocidad = random.uniform(0.8, 1.5)
        self.alpha = 180
        # Colores vibrantes para las partículas
        colores_particula = [
            (255, 100, 100), (100, 255, 100), (100, 100, 255),
            (255, 255, 100), (255, 100, 255), (100, 255, 255)
        ]
        self.color = random.choice(colores_particula)

    def actualizar(self):
        self.x -= self.velocidad
        self.y -= 0.2
        self.alpha -= 4
        return self.alpha > 0

    def dibujar(self, pantalla):
        if self.alpha > 0:
            superficie = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
            color_con_alpha = (*self.color, self.alpha)
            pygame.draw.circle(superficie, color_con_alpha,
                               (self.radio, self.radio), self.radio)
            pantalla.blit(superficie, (self.x - self.radio, self.y - self.radio))


class SeleccionPersonaje:
    # MODIFICADO: Añadido arduino_serial=None e idioma
    def __init__(self, pantalla, ancho, alto, arduino_serial=None, idioma="es"):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.arduino_serial = arduino_serial # <-- MODIFICADO
        self.idioma = idioma

        # --- Textos Multi-idioma (MODIFICADO) ---
        self.textos = {
            "es": {
                "titulo": "Selecciona tu personaje",
                "perro": "Perro",
                "gato": "Gato",
                "volver": "VOLVER",
                "instruccion1": "Use 'Flecha Izquierda' para cambiar.",
                "instruccion2": "Use 'Flecha Abajo' para Volver. Use 'Flecha Derecha' para confirmar."
            },
            "en": {
                "titulo": "Select your character",
                "perro": "Dog",
                "gato": "Cat",
                "volver": "BACK",
                "instruccion1": "Use 'Left Arrow' to change.",
                "instruccion2": "Use 'Down Arrow' for Back. Use 'Right Arrow' to confirm."
            }
        }
        self.actualizar_textos() # Asegurar que los textos se carguen correctamente

        # --- Fuentes ---
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_nombre = pygame.font.Font(None, 60)
        self.fuente_volver = pygame.font.Font(None, 55)
        # MODIFICADO: Fuente para instrucciones más grande
        self.fuente_instruccion = pygame.font.Font(None, 35)

        # --- Colores vibrantes ---
        self.color_marco = (100, 150, 255)  # Azul brillante
        self.color_hover = (255, 100, 50)   # Naranja vibrante
        self.color_texto = (255, 255, 255)
        self.color_sombra = (0, 0, 0)
        self.color_titulo = (255, 255, 100)   # Amarillo estándar
        self.color_fondo_top = (20, 40, 80) # Azul oscuro
        self.color_fondo_bottom = (80, 20, 60) # Morado oscuro

        # --- Fondo ---
        ruta_base = os.path.join(os.path.dirname(__file__), "..", "img")
        self.fondo = pygame.image.load(os.path.join(ruta_base, "fondo.png")).convert()
        self.fondo = pygame.transform.scale(self.fondo, (ancho, alto))

        # Brillitos del selector de personajes
        self.brillitos_selector = []
        for _ in range(35):
            self.brillitos_selector.append({
                'x': random.randint(0, ancho),
                'y': random.randint(0, alto),
                'vx': random.uniform(-0.6, 0.6),
                'vy': random.uniform(-0.6, 0.6),
                'color': random.choice([
                    (255, 255, 100),  # Amarillo brillante
                    (100, 255, 255),  # Cyan brillante
                    (255, 100, 255),  # Magenta brillante
                    (100, 255, 100),  # Verde brillante
                    (255, 255, 100),  # Amarillo estándar
                    (200, 100, 255),  # Púrpura brillante
                ]),
                'size': random.randint(1, 3),
                'vida': random.randint(80, 250),
                'vida_max': random.randint(80, 250)
            })

        # --- Animaciones (MODIFICADO: Escalado a 200px) ---
        self.frames_perro = escalar_lista(
            [escalar_y_cuadrar(cargar_imagen(f"perro_run{i}.png"), 200) for i in range(1, 5)], 200, 200
        )
        self.frames_gato = escalar_lista(
            [escalar_y_cuadrar(cargar_imagen(f"gato_run{i}.png"), 200) for i in range(1, 5)], 200, 200
        )

        # --- Control de frames ---
        self.frame_index_perro = 0
        self.frame_index_gato = 0
        self.frame_timer = 0

        # --- Polvo (efecto animado) ---
        self.polvos_perro = []
        self.polvos_gato = []

        self.opciones = ["perro", "gato", "volver"]
        self.opcion_sel = 0 # 0 = Perro, 1 = Gato, 2 = Volver

    def actualizar_textos(self):
        """Actualiza los textos según el idioma actual"""
        self.txt = self.textos[self.idioma]

    def dibujar_texto(self, texto, fuente, color, x, y, sombra=True, centrado=True):
        if sombra:
            sombra_surface = fuente.render(texto, True, self.color_sombra)
            sombra_rect = sombra_surface.get_rect(center=(x + 3, y + 3))
            if centrado:
                self.pantalla.blit(sombra_surface, sombra_rect)
            else:
                 self.pantalla.blit(sombra_surface, (sombra_rect.x, sombra_rect.y))
        texto_surface = fuente.render(texto, True, color)
        rect = texto_surface.get_rect(center=(x, y)) if centrado else texto_surface.get_rect(topleft=(x, y))
        self.pantalla.blit(texto_surface, rect)

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
            pygame.draw.line(self.pantalla, color, (0, y), (self.ancho, y))
        
        # Añadir estrellas coloridas estáticas
        estrellas_positions = [
            (80, 120), (320, 60), (520, 180), (720, 100),
            (120, 380), (480, 320), (680, 420), (180, 280),
            (580, 480), (380, 160), (780, 280), (30, 230)
        ]
        
        colores_estrellas = [
            (255, 150, 150), (150, 255, 150), (150, 150, 255),
            (255, 255, 150), (255, 150, 255), (150, 255, 255)
        ]
        
        for i, pos in enumerate(estrellas_positions):
            if pos[0] < self.ancho and pos[1] < self.alto:
                color = colores_estrellas[i % len(colores_estrellas)]
                pygame.draw.circle(self.pantalla, color, pos, 3)

    def dibujar_tarjeta(self, nombre, imagen, x, y, seleccionado=False, polvos=None):
        # MODIFICADO: Tarjetas más pequeñas con colores vibrantes
        ancho_card, alto_card = 240, 320 
        card_rect = pygame.Rect(x - ancho_card // 2, y - alto_card // 2, ancho_card, alto_card)

        superficie_card = pygame.Surface((ancho_card, alto_card), pygame.SRCALPHA)
        
        if seleccionado:
            # Colores vibrantes para tarjeta seleccionada
            color_base = (60, 100, 150, 220)  # Azul vibrante
            color_borde = self.color_hover  # Naranja vibrante
        else:
            color_base = (40, 60, 80, 200)  # Azul grisáceo
            color_borde = self.color_marco  # Azul brillante
        
        pygame.draw.rect(superficie_card, color_base, (0, 0, ancho_card, alto_card), border_radius=20)
        pygame.draw.rect(superficie_card, color_borde, (0, 0, ancho_card, alto_card), 4, border_radius=20)

        # Sin sombra - directamente dibujamos la superficie
        self.pantalla.blit(superficie_card, (card_rect.x, card_rect.y))

        # --- Dibujar polvo colorido debajo ---
        if polvos is not None:
            for p in polvos[:]:
                if not p.actualizar():
                    polvos.remove(p)
                else:
                    p.dibujar(self.pantalla)

        # --- Imagen del personaje ---
        img_rect = imagen.get_rect(center=(x, y - 30))
        self.pantalla.blit(imagen, img_rect)

        # --- Nombre ---
        color_texto = self.color_hover if seleccionado else self.color_texto
        self.dibujar_texto(nombre.upper(), self.fuente_nombre, color_texto, x, y + 100) # Ajustado Y

        if seleccionado:
            brillo = pygame.Surface((ancho_card, alto_card), pygame.SRCALPHA)
            pygame.draw.rect(brillo, (255, 255, 255, 25), (0, 0, ancho_card, alto_card), border_radius=20)
            self.pantalla.blit(brillo, (card_rect.x, card_rect.y))

    def actualizar_brillitos(self):
        """Actualiza los brillitos del selector"""
        for brillito in self.brillitos_selector:
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
        """Dibuja los brillitos del selector"""
        for brillito in self.brillitos_selector:
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
            
            self.pantalla.blit(surf, (int(brillito['x']) - tamano//2, int(brillito['y']) - tamano//2))

    def mostrar(self):
        clock = pygame.time.Clock()
        anim = 0
        direccion = 1

        while True:
            # Fondo colorido vibrante
            self.dibujar_fondo_colorido()
            
            # Actualizar y dibujar brillitos
            self.actualizar_brillitos()
            self.dibujar_brillitos()

            # Título dorado con sombra
            self.dibujar_texto(self.txt["titulo"], self.fuente_titulo,
                               self.color_titulo, self.ancho // 2, 80, sombra=True)

            if anim > 10 or anim < -10:
                direccion *= -1
            anim += direccion * 0.5

            self.frame_timer += 1
            if self.frame_timer >= 10:
                self.frame_timer = 0
                self.frame_index_perro = (self.frame_index_perro + 1) % len(self.frames_perro)
                self.frame_index_gato = (self.frame_index_gato + 1) % len(self.frames_gato)

                # Generar polvo cada cambio de frame
                self.polvos_perro.append(Polvo(self.ancho // 2 - 200, self.alto // 2 + 120))
                self.polvos_gato.append(Polvo(self.ancho // 2 + 200, self.alto // 2 + 120))

            perro_img = self.frames_perro[self.frame_index_perro]
            gato_img = self.frames_gato[self.frame_index_gato]

            # MODIFICADO: centro_y subido
            centro_y = self.alto // 2 
            sep_x = 180 # Más cerca
            x_perro = self.ancho // 2 - sep_x
            x_gato = self.ancho // 2 + sep_x

            self.dibujar_tarjeta(self.txt["perro"], perro_img, x_perro,
                                 centro_y + (anim if self.opcion_sel == 0 else 0),
                                 seleccionado=(self.opcion_sel == 0),
                                 polvos=self.polvos_perro)
            self.dibujar_tarjeta(self.txt["gato"], gato_img, x_gato,
                                 centro_y + (anim if self.opcion_sel == 1 else 0),
                                 seleccionado=(self.opcion_sel == 1),
                                 polvos=self.polvos_gato)

            # ------------------------------------
            # ⬇️ DIBUJAR INSTRUCCIONES COLORIDAS (MODIFICADO) ⬇️
            # ------------------------------------
            color_inst = (255, 255, 100)  # Amarillo estándar
            self.dibujar_texto(self.txt["instruccion1"], 
                               self.fuente_instruccion, 
                               color_inst, 
                               self.ancho // 2, 
                               centro_y + 190, # Debajo de las tarjetas
                               sombra=True) # Activar sombra
            self.dibujar_texto(self.txt["instruccion2"], 
                               self.fuente_instruccion, 
                               color_inst,
                               self.ancho // 2, 
                               centro_y + 225, # Debajo de las tarjetas
                               sombra=True) # Activar sombra
            # ------------------------------------
            # ⬆️ FIN INSTRUCCIONES ⬆️
            # ------------------------------------


            # --- Botón VOLVER colorido (abajo centrado) ---
            boton_ancho, boton_alto = 200, 65
            boton_x = self.ancho // 2 - boton_ancho // 2
            boton_y = self.alto - 100
            boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)

            if self.opcion_sel == 2:
                color_btn = (100, 50, 150)    # Morado vibrante
                color_borde = (255, 100, 255) # Magenta
                color_texto = (255, 255, 255)
            else:
                color_btn = (50, 80, 120)     # Azul oscuro
                color_borde = (100, 150, 255) # Azul claro
                color_texto = (200, 200, 255)
            
            pygame.draw.rect(self.pantalla, color_btn, boton_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, color_borde, boton_rect, 3, border_radius=20)
            self.dibujar_texto(self.txt["volver"], self.fuente_volver, color_texto,
                               boton_rect.centerx, boton_rect.centery)

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


            # --- Eventos (MODIFICADOS PARA ARDUINO) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.arduino_serial and self.arduino_serial.is_open:
                        self.arduino_serial.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_DOWN: # D4
                        if self.opcion_sel == 0 or self.opcion_sel == 1:
                            self.opcion_sel = 2 # Ir a Volver
                    
                    elif event.key == pygame.K_UP: # D2
                        if self.opcion_sel == 2:
                            self.opcion_sel = 0 # Ir a Perro
                    
                    elif event.key == pygame.K_LEFT: # D5
                        if self.opcion_sel == 1:
                            self.opcion_sel = 0 # Gato -> Perro
                        elif self.opcion_sel == 0:
                            self.opcion_sel = 1 # Perro -> Gato
                        elif self.opcion_sel == 2:
                            return "volver" # Si estás en Volver, K_LEFT (D5) te saca

                    elif event.key == pygame.K_RIGHT: # D3
                        # K_RIGHT (D3) es CONFIRMAR
                        return self.opciones[self.opcion_sel] # Confirma Perro, Gato, o Volver

                    elif event.key == pygame.K_RETURN: # Mantener Enter
                        return self.opciones[self.opcion_sel]
                    
                    elif event.key == pygame.K_ESCAPE: # Mantener Escape
                        return "volver"

            pygame.display.flip()
            clock.tick(60)