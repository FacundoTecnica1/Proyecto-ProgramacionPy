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

    def actualizar(self):
        self.x -= self.velocidad
        self.y -= 0.2
        self.alpha -= 4
        return self.alpha > 0

    def dibujar(self, pantalla):
        if self.alpha > 0:
            superficie = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie, (255, 255, 255, self.alpha),
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

        # --- Colores ---
        self.color_marco = (220, 220, 220)
        self.color_hover = (255, 255, 255)
        self.color_texto = (230, 230, 230)
        self.color_sombra = (0, 0, 0)

        # --- Fondo ---
        ruta_base = os.path.join(os.path.dirname(__file__), "..", "img")
        self.fondo = pygame.image.load(os.path.join(ruta_base, "fondo.png")).convert()
        self.fondo = pygame.transform.scale(self.fondo, (ancho, alto))

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

    def dibujar_tarjeta(self, nombre, imagen, x, y, seleccionado=False, polvos=None):
        # MODIFICADO: Tarjetas más pequeñas
        ancho_card, alto_card = 240, 320 
        card_rect = pygame.Rect(x - ancho_card // 2, y - alto_card // 2, ancho_card, alto_card)

        superficie_card = pygame.Surface((ancho_card, alto_card), pygame.SRCALPHA)
        color_base = (40, 40, 40, 200) if not seleccionado else (80, 80, 80, 220)
        pygame.draw.rect(superficie_card, color_base, (0, 0, ancho_card, alto_card), border_radius=20)
        
        color_borde = self.color_hover if seleccionado else self.color_marco
        pygame.draw.rect(superficie_card, color_borde, (0, 0, ancho_card, alto_card), 4, border_radius=20)

        sombra = pygame.Surface((ancho_card + 10, alto_card + 10), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 100))
        self.pantalla.blit(sombra, (card_rect.x + 4, card_rect.y + 4))
        self.pantalla.blit(superficie_card, (card_rect.x, card_rect.y))

        # --- Dibujar polvo debajo ---
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

    def mostrar(self):
        clock = pygame.time.Clock()
        anim = 0
        direccion = 1

        while True:
            self.pantalla.blit(self.fondo, (0, 0))

            self.dibujar_texto(self.txt["titulo"], self.fuente_titulo,
                               (255, 255, 255), self.ancho // 2, 80) # Subido

            if anim > 10 or anim < -10:
                direccion *= -1
            anim += direccion * 0.5

            self.frame_timer += 1
            if self.frame_timer >= 10:
                self.frame_timer = 0
                self.frame_index_perro = (self.frame_index_perro + 1) % len(self.frames_perro)
                self.frame_index_gato = (self.frame_index_gato + 1) % len(self.frames_gato)

                # Generar polvo cada cambio de frame
                self.polvos_perro.append(Polvo(self.ancho // 2 - 200, self.alto // 2 + 120)) # Subido
                self.polvos_gato.append(Polvo(self.ancho // 2 + 200, self.alto // 2 + 120)) # Subido

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
            # ⬇️ DIBUJAR INSTRUCCIONES (MODIFICADO) ⬇️
            # ------------------------------------
            color_inst = (255, 230, 150) # Amarillo brillante
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


            # --- Botón VOLVER (abajo centrado) ---
            boton_ancho, boton_alto = 200, 65
            boton_x = self.ancho // 2 - boton_ancho // 2
            boton_y = self.alto - 100
            boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)

            color_btn = (50, 50, 50)
            color_borde = (255, 255, 255)
            if self.opcion_sel == 2:
                color_btn = (100, 100, 100)
                color_borde = self.color_hover
            
            pygame.draw.rect(self.pantalla, color_btn, boton_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, color_borde, boton_rect, 3, border_radius=20)
            self.dibujar_texto(self.txt["volver"], self.fuente_volver, (255, 255, 255),
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