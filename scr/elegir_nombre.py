import pygame
import sys
import os
import math
import mysql.connector
import serial # <-- MODIFICADO: Importado
import random  # Para los efectos de brillitos

class ElegirNombre:
    # MODIFICADO: Añadido arduino_serial=None e idioma="es"
    def __init__(self, pantalla, ancho, alto, arduino_serial=None, idioma="es"):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.arduino_serial = arduino_serial # <-- MODIFICADO
        self.idioma = idioma # <-- MODIFICADO

        # Variables para el mensaje de error
        self.mostrar_error = False
        self.tiempo_error = 0
        self.duracion_error = 2000  # 2 segundos

        # Estilo visual vibrante
        self.color_texto = (255, 255, 255)
        self.color_resaltado = (255, 100, 50)      # Naranja vibrante
        self.color_fondo = (25, 25, 35)
        self.color_titulo = (255, 255, 100)          # Amarillo estándar
        self.color_letra_activa = (100, 255, 255)  # Cyan vibrante
        self.color_letra_normal = (200, 200, 255)  # Azul claro
        self.color_casilla_activa = (255, 100, 100) # Rojo vibrante
        self.color_casilla_normal = (50, 80, 120)  # Azul oscuro
        self.color_instrucciones = (255, 200, 150) # Naranja suave
        self.fuente_titulo = pygame.font.Font(None, 100)
        self.fuente_letra = pygame.font.Font(None, 120)
        self.fuente_info = pygame.font.Font(None, 40)
        # MODIFICADO: Fuente para instrucciones más grande
        self.fuente_instruccion = pygame.font.Font(None, 35) 
        self.anim_tiempo = 0

        # Efectos de brillitos
        self.brillitos = []
        for _ in range(50):
            self.brillitos.append({
                'x': random.randint(0, ancho),
                'y': random.randint(0, alto),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'color': random.choice([
                    (255, 255, 100),  # Amarillo brillante
                    (100, 255, 255),  # Cyan brillante
                    (255, 100, 255),  # Magenta brillante
                    (100, 255, 100),  # Verde brillante
                    (255, 255, 100),  # Amarillo estándar
                    (200, 100, 255),  # Púrpura brillante
                ]),
                'size': random.randint(1, 3),
                'vida': random.randint(100, 300),
                'vida_max': random.randint(100, 300)
            })

        # --- Textos Multi-idioma (MODIFICADO) ---
        self.textos = {
            "es": {
                "titulo": "ELIGE TU NOMBRE",
                "instruccion1": "Use 'Flecha Arriba'/'Flecha Abajo' para cambiar la letra.",
                "instruccion2": "Use 'Flecha Izquierda'/'Flecha Derecha' para mover la casilla.",
                "instruccion3": "Confirme con 'Flecha Derecha' en la última casilla.",
                "error_nombre": "¡Nombre ya en uso! Elige otro nombre."
            },
            "en": {
                "titulo": "CHOOSE YOUR NAME",
                "instruccion1": "Use 'Up Arrow'/'Down Arrow' to change letter.",
                "instruccion2": "Use 'Left Arrow'/'Right Arrow' to move slot.",
                "instruccion3": "Confirm with 'Right Arrow' on the last slot.",
                "error_nombre": "Name already taken! Choose another name."
            }
        }
        self.txt = self.textos[self.idioma]

        # Fondo opcional
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
        if os.path.exists(ruta_fondo):
            self.fondo_img = pygame.image.load(ruta_fondo).convert()
            self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))
        else:
            self.fondo_img = None

        # Letras y estado
        self.letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.indice = [0, 0, 0, 0]
        self.posicion_actual = 0

        # Base de datos
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "dino"
        }

        # Crear tablas si no existen
        self.crear_tablas()

        # Cargar último nombre
        self.nombre_guardado = self.obtener_nombre_guardado()
        if self.nombre_guardado:
            self.cargar_nombre_guardado(self.nombre_guardado)

        # Id del usuario actual
        self.id_usuario_actual = None

    # ============================
    # BASE DE DATOS
    # ============================
    def crear_tablas(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    Id_Usuario INT AUTO_INCREMENT PRIMARY KEY,
                    Nombre VARCHAR(50) NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ranking (
                    Id_Ranking INT AUTO_INCREMENT PRIMARY KEY,
                    Id_Usuario INT NOT NULL,
                    Puntaje INT NOT NULL,
                    FOREIGN KEY (Id_Usuario) REFERENCES usuario(Id_Usuario)
                );
            """)
            conexion.commit()
            conexion.close()
        except Exception as e:
            print(f"[ERROR DB] {e}")

    def guardar_nombre(self, nombre):
        """Guarda el nombre en la base de datos y devuelve su ID"""
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuario (Nombre) VALUES (%s);", (nombre,))
            conexion.commit()
            self.id_usuario_actual = cursor.lastrowid
            conexion.close()
            print(f"[INFO] Usuario '{nombre}' guardado con ID {self.id_usuario_actual}")
            return self.id_usuario_actual
        except Exception as e:
            print(f"[ERROR DB] {e}")
            return None # Retornar None en caso de error

    def obtener_nombre_guardado(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            cursor.execute("SELECT Nombre FROM usuario ORDER BY Id_Usuario DESC LIMIT 1;")
            fila = cursor.fetchone()
            conexion.close()
            return fila[0] if fila else None
        except Exception as e:
            print(f"[ERROR DB] {e}")
            return None
    def nombre_existe(self, nombre):
        """Verifica si un nombre ya existe en la base de datos"""
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            # Comparar en mayúsculas para evitar diferencias de case
            cursor.execute("SELECT COUNT(*) FROM usuario WHERE UPPER(Nombre) = %s", (nombre.upper(),))
            count = cursor.fetchone()[0]
            conexion.close()
            return count > 0
        except Exception as e:
            print(f"Error al verificar nombre: {e}")
            return False

    # ============================
    # FONDO ANIMADO
    # ============================
    def gradiente_fondo(self):
        """Fondo animado tipo aurora, sin errores de color"""
        self.anim_tiempo += 0.015

        for y in range(self.alto):
            r = 40 + int(40 * math.sin(self.anim_tiempo + y * 0.008))
            g = 20 + int(30 * math.sin(self.anim_tiempo * 0.6 + y * 0.015))
            b = 80 + int(50 * math.cos(self.anim_tiempo + y * 0.01))

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            pygame.draw.line(self.pantalla, (r, g, b), (0, y), (self.ancho, y))

    # ============================
    # INTERFAZ
    # ============================
    def cargar_nombre_guardado(self, nombre):
        nombre = nombre.upper()[:4]
        for i, letra in enumerate(nombre):
            if letra in self.letras:
                self.indice[i] = self.letras.index(letra)

    # MODIFICADO: Añadido dibujar texto simple (con sombra)
    def actualizar_brillitos(self):
        """Actualiza y dibuja los efectos de brillitos"""
        for brillito in self.brillitos:
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
            
            # Calcular alpha basado en la vida
            alpha = int(255 * (brillito['vida'] / brillito['vida_max']))
            
            # Crear superficie con alpha para el brillito
            tamano = brillito['size'] * 4
            surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
            
            # Dibujar círculo principal
            pygame.draw.circle(surf, brillito['color'], (tamano//2, tamano//2), brillito['size'])
            
            # Efecto de brillo adicional (círculo más pequeño y brillante)
            color_brillo = tuple(min(255, c + 50) for c in brillito['color'])
            pygame.draw.circle(surf, color_brillo, (tamano//2, tamano//2), max(1, brillito['size']//2))
            
            # Aplicar alpha a toda la superficie
            surf.set_alpha(alpha)
            
            self.pantalla.blit(surf, (int(brillito['x']) - tamano//2, int(brillito['y']) - tamano//2))

    def dibujar_texto_simple(self, texto, fuente, color, x, y, centrado=True, sombra_color=(0,0,0)):
        # Sombra
        sombra_surf = fuente.render(texto, True, sombra_color)
        sombra_rect = sombra_surf.get_rect(center=(x + 2, y + 2)) if centrado else sombra_surf.get_rect(topleft=(x + 2, y + 2))
        self.pantalla.blit(sombra_surf, sombra_rect)
        
        # Texto
        surf = fuente.render(texto, True, color)
        rect = surf.get_rect(center=(x, y)) if centrado else surf.get_rect(topleft=(x, y))
        self.pantalla.blit(surf, rect)

    def dibujar_fondo_colorido(self):
        """Dibuja un fondo colorido con estrellas como los otros menús"""
        # Fondo degradado estático
        if self.fondo_img:
            self.pantalla.blit(self.fondo_img, (0, 0))
        else:
            self.gradiente_fondo()
        
        # Añadir estrellas coloridas estáticas
        estrellas_positions = [
            (80, 120), (320, 60), (520, 180), (720, 100),
            (120, 380), (480, 320), (680, 420), (180, 280),
            (580, 480), (380, 160), (780, 280), (30, 230),
            (650, 150), (250, 400), (750, 350), (150, 50)
        ]
        
        colores_estrellas = [
            (255, 255, 100), (100, 255, 255), (255, 100, 255),
            (100, 255, 100), (255, 255, 100), (200, 100, 255)
        ]
        
        for i, pos in enumerate(estrellas_positions):
            if pos[0] < self.ancho and pos[1] < self.alto:
                color = colores_estrellas[i % len(colores_estrellas)]
                # Dibujar estrella como un círculo con rayos
                pygame.draw.circle(self.pantalla, color, pos, 3)
                # Rayos de la estrella
                pygame.draw.line(self.pantalla, color, (pos[0]-6, pos[1]), (pos[0]+6, pos[1]), 1)
                pygame.draw.line(self.pantalla, color, (pos[0], pos[1]-6), (pos[0], pos[1]+6), 1)

    def mostrar(self):
        clock = pygame.time.Clock()

        while True:
            # Fondo colorido con estrellas
            self.dibujar_fondo_colorido()
            
            # Actualizar y dibujar brillitos
            self.actualizar_brillitos()

            # Título colorido
            # MODIFICADO: Usar self.txt y color dorado
            titulo_texto = self.txt["titulo"]
            sombra = self.fuente_titulo.render(titulo_texto, True, (100, 50, 0))  # Sombra dorada oscura
            texto = self.fuente_titulo.render(titulo_texto, True, self.color_titulo)  # Dorado
            rect = texto.get_rect(center=(self.ancho // 2, 120))
            self.pantalla.blit(sombra, (rect.x + 3, rect.y + 3))
            self.pantalla.blit(texto, rect)

            # Letras coloridas
            inicio_x = self.ancho // 2 - 1.5 * 140
            pos_y_letras = self.alto // 2
            for i in range(4):
                letra = self.letras[self.indice[i]]
                
                # Colores vibrantes según si está activa o no
                if i == self.posicion_actual:
                    color_letra = self.color_letra_activa    # Cyan vibrante
                    color_caja = self.color_casilla_activa   # Rojo vibrante
                else:
                    color_letra = self.color_letra_normal    # Azul claro
                    color_caja = self.color_casilla_normal   # Azul oscuro
                
                surf = self.fuente_letra.render(letra, True, color_letra)
                rect = surf.get_rect(center=(inicio_x + i * 140, pos_y_letras))

                # Cuadro colorido sin sombra
                caja_rect = rect.inflate(50, 50)
                pygame.draw.rect(self.pantalla, color_caja, caja_rect, border_radius=15)
                pygame.draw.rect(self.pantalla, color_letra, caja_rect, 3, border_radius=15)
                self.pantalla.blit(surf, rect)

            # ------------------------------------
            # ⬇️ DIBUJAR INSTRUCCIONES COLORIDAS (MODIFICADO) ⬇️
            # ------------------------------------
            self.dibujar_texto_simple(self.txt["instruccion1"], 
                                      self.fuente_instruccion, 
                                      self.color_instrucciones, 
                                      self.ancho // 2, 
                                      pos_y_letras + 120)
            self.dibujar_texto_simple(self.txt["instruccion2"], 
                                      self.fuente_instruccion, 
                                      self.color_instrucciones, 
                                      self.ancho // 2, 
                                      pos_y_letras + 160)
            self.dibujar_texto_simple(self.txt["instruccion3"], 
                                      self.fuente_instruccion, 
                                      self.color_instrucciones, 
                                      self.ancho // 2, 
                                      pos_y_letras + 200)
            # ------------------------------------
            # ⬆️ FIN INSTRUCCIONES ⬆️
            # ------------------------------------

           
            # Efectos visuales suaves
            overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            overlay.fill((10, 10, 30, 30))
            self.pantalla.blit(overlay, (0, 0))

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
                        elif linea == "UP_UP":
                            evento_tipo = pygame.KEYUP
                            evento_key = pygame.K_UP
                        elif linea == "DOWN_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_DOWN
                        elif linea == "DOWN_UP":
                            evento_tipo = pygame.KEYUP
                            evento_key = pygame.K_DOWN
                        elif linea == "LEFT_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_LEFT
                        elif linea == "LEFT_UP":
                            evento_tipo = pygame.KEYUP
                            evento_key = pygame.K_LEFT
                        elif linea == "RIGHT_DOWN":
                            evento_tipo = pygame.KEYDOWN
                            evento_key = pygame.K_RIGHT
                        elif linea == "RIGHT_UP":
                            evento_tipo = pygame.KEYUP
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

            # Controles
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.arduino_serial and self.arduino_serial.is_open:
                        self.arduino_serial.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.indice[self.posicion_actual] = (self.indice[self.posicion_actual] + 1) % len(self.letras)
                    elif event.key == pygame.K_DOWN:
                        self.indice[self.posicion_actual] = (self.indice[self.posicion_actual] - 1) % len(self.letras)
                    elif event.key == pygame.K_RIGHT:
                        if self.posicion_actual == 3:  # Confirmar nombre
                            nombre = "".join([self.letras[i] for i in self.indice])
                            # Verificar duplicado (mayúsculas)
                            if self.nombre_existe(nombre):
                                self.mostrar_error = True
                                self.tiempo_error = pygame.time.get_ticks()
                            else:
                                id_usuario = self.guardar_nombre(nombre)
                                return nombre, id_usuario
                        else:
                            self.posicion_actual = (self.posicion_actual + 1) % 4
                    elif event.key == pygame.K_LEFT:
                        self.posicion_actual = (self.posicion_actual - 1) % 4
            # Mostrar mensaje de error si es necesario
            if self.mostrar_error:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.tiempo_error > self.duracion_error:
                    self.mostrar_error = False
                else:
                    # Superficie del mensaje (fondo amarillo, texto oscuro)
                    mensaje_surf = pygame.Surface((600, 70), pygame.SRCALPHA)
                    pygame.draw.rect(mensaje_surf, (255, 215, 100, 220), mensaje_surf.get_rect(), border_radius=12)
                    texto_error = self.fuente_info.render(self.txt.get("error_nombre", "Nombre en uso"), True, (30,30,30))
                    texto_rect = texto_error.get_rect(center=(mensaje_surf.get_width()//2, mensaje_surf.get_height()//2))
                    mensaje_surf.blit(texto_error, texto_rect)
                    # Posicionar el mensaje más abajo en la pantalla
                    pos_y_mensaje = self.alto - 100
                    rect_mensaje = mensaje_surf.get_rect(center=(self.ancho//2, pos_y_mensaje))
                    self.pantalla.blit(mensaje_surf, rect_mensaje)

            pygame.display.flip()
            clock.tick(60)