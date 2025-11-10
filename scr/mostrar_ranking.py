import pygame
import pymysql
import sys
import os
import serial # <-- MODIFICADO: Importado

# --- RUTAS PARA PYINSTALLER ---
if getattr(sys, 'frozen', False):
    RUTA_BASE = os.path.join(sys._MEIPASS, "img")
else:
    RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

# Ruta de la aplicación (donde escribir logs). Si está congelado por PyInstaller,
# escribir junto al ejecutable, sino junto al archivo .py
if getattr(sys, 'frozen', False):
    RUTA_APP = os.path.dirname(sys.executable)
else:
    RUTA_APP = os.path.dirname(__file__)

def write_log(msg: str):
    """Intenta escribir una línea en rank_debug.log junto al ejecutable (silencioso si falla)."""
    try:
        with open(os.path.join(RUTA_APP, "rank_debug.log"), "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        # No fallar la ejecución del juego por el logging
        pass

# Señal de que el módulo fue cargado (útil para distinguir si el exe está usando esta versión)
try:
    write_log("[INFO] mostrar_ranking module cargado")
except Exception:
    pass

class MostrarRanking:
    # MODIFICADO: Añadido arduino_serial=None e idioma
    def __init__(self, pantalla, ancho, alto, arduino_serial=None, idioma="es"):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.arduino_serial = arduino_serial # <-- MODIFICADO
        self.idioma = idioma

        # --- Textos Multi-idioma ---
        self.textos = {
            "es": {
                "titulo": "Top 3 Records",
                "no_records": "No hay récords todavía",
                "volver": "VOLVER"
            },
            "en": {
                "titulo": "Top 3 High Scores",
                "no_records": "No records yet",
                "volver": "BACK"
            }
        }
        self.txt = self.textos[self.idioma]

        # --- Fuentes estilo arcade ---
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_nombre = pygame.font.Font(None, 65)
        self.fuente_puntaje = pygame.font.Font(None, 55)
        self.fuente_info = pygame.font.Font(None, 35)
        self.fuente_boton = pygame.font.Font(None, 55)

        # --- Colores vibrantes ---
        self.color_titulo = (255, 255, 100)      # Amarillo estándar
        self.color_nombre = (100, 255, 255)    # Cyan vibrante
        self.color_puntaje = (255, 100, 100)   # Rojo vibrante
        self.color_sombra = (0, 0, 0)
        self.color_boton = (50, 80, 120)       # Azul oscuro
        self.color_boton_hover = (255, 100, 50) # Naranja vibrante
        self.color_fondo_top = (20, 30, 60)    # Azul muy oscuro
        self.color_fondo_bottom = (60, 20, 40) # Morado oscuro

        # --- Fondo e imágenes ---
        self.fondo = pygame.image.load(os.path.join(RUTA_BASE, "fondo2.png")).convert()  # Fondo de día
        self.fondo = pygame.transform.scale(self.fondo, (ancho, alto))

        self.medalla_oro = pygame.image.load(os.path.join(RUTA_BASE, "oro.png")).convert_alpha()
        self.medalla_plata = pygame.image.load(os.path.join(RUTA_BASE, "plata.png")).convert_alpha()
        self.medalla_bronce = pygame.image.load(os.path.join(RUTA_BASE, "bronce.png")).convert_alpha()

        # --- Conexión BD ---
        write_log("[INFO] Intentando conectar a MySQL con PyMySQL...")
        
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="dino",
                connect_timeout=3,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.Cursor
            )
            self.cursor = self.conn.cursor()
            print("[OK] Conectado a la base de datos MySQL (PyMySQL)")
            write_log("[OK] Conectado a la base de datos MySQL (PyMySQL)")
        except Exception as e:
            print(f"[ERROR DB] No se pudo conectar a MySQL: {e}")
            print("[INFO] El juego funcionará sin ranking persistente")
            write_log(f"[ERROR DB] No se pudo conectar a MySQL: {e}")
            write_log(f"[ERROR DB] Tipo de error: {type(e).__name__}")
            import traceback
            write_log(f"[ERROR DB] Traceback: {traceback.format_exc()}")
            self.conn = None
            self.cursor = None
        write_log(f"[INFO] Cursor inicializado: {self.cursor is not None}")

    def obtener_top3(self):
        print(f"[DEBUG] obtener_top3 llamado. cursor existe: {self.cursor is not None}")
        if not self.cursor:
            print("[DEBUG] No hay cursor, retornando lista vacía")
            write_log("[DEBUG] obtener_top3 llamado pero no hay cursor, lista vacía")
            return []
        try:
            self.cursor.execute("""
                SELECT u.Nombre, r.Puntaje
                FROM ranking r
                JOIN usuario u ON r.Id_Usuario = u.Id_Usuario
                ORDER BY r.Puntaje DESC
                LIMIT 3
            """)
            resultados = self.cursor.fetchall()
            print(f"[DEBUG] Resultados obtenidos: {resultados}")
            write_log(f"[DEBUG] Resultados obtenidos: {resultados}")
            return resultados
        except Exception as e:
            print(f"[ERROR SQL] {e}")
            write_log(f"[ERROR SQL] {e}")
            return []

    def dibujar_texto_con_sombra(self, texto, fuente, color, x, y, centro=False):
        # Verificar que el texto no sea None
        if texto is None:
            texto = "Sin nombre"
        # Convertir a string si no lo es
        texto = str(texto)
        
        sombra = fuente.render(texto, True, self.color_sombra)
        render = fuente.render(texto, True, color)
        
        if centro:
            rect = render.get_rect(center=(x, y))
            sombra_rect = sombra.get_rect(center=(x + 3, y + 3))
        else:
            rect = (x, y)
            sombra_rect = (x + 3, y + 3)
            
        self.pantalla.blit(sombra, sombra_rect)
        self.pantalla.blit(render, rect)

    def dibujar_fondo_colorido(self):
        """Dibuja el fondo de día con estrellas coloridas"""
        # Fondo de día como base
        self.pantalla.blit(self.fondo, (0, 0))
        
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
        glow = 0
        glow_dir = 1
        boton_rect = pygame.Rect(self.ancho // 2 - 120, self.alto - 100, 240, 70)
        
        # En esta pantalla, el botón "Volver" está siempre seleccionado
        seleccionado = True 

        while True:
            # Fondo colorido vibrante con estrellas
            self.dibujar_fondo_colorido()

            # --- Título principal colorido ---
            self.dibujar_texto_con_sombra(self.txt["titulo"],
                                          self.fuente_titulo,
                                          self.color_titulo,
                                          self.ancho // 2, 90, centro=True)

            top3 = self.obtener_top3()

            # Registrar en log lo que el exe obtuvo para poder diagnosticar diferencias
            try:
                write_log(f"[DEBUG] mostrar loop top3: {top3}")
            except Exception:
                pass

            if not top3:
                self.dibujar_texto_con_sombra(self.txt["no_records"],
                                              self.fuente_info,
                                              self.color_titulo,
                                              self.ancho // 2,
                                              self.alto // 2, centro=True)
            else:
                posiciones = [
                    (self.ancho // 2, 270),     
                    (self.ancho // 2 - 280, 380),
                    (self.ancho // 2 + 280, 380)
                ]
                medallas = [self.medalla_oro, self.medalla_plata, self.medalla_bronce]
                tamanios_medalla = [(160, 180), (150, 170), (150, 170)]

                for i, (nombre, puntaje) in enumerate(top3):
                    if i >= len(top3): break # Seguridad
                        
                    x, y = posiciones[i]
                    
                    # Verificar valores None
                    if nombre is None:
                        nombre = "Sin nombre"
                    if puntaje is None:
                        puntaje = 0

                    # Cuadro
                    cuadro = pygame.Surface((260, 130), pygame.SRCALPHA)
                    pygame.draw.rect(cuadro, (30, 30, 30, 220), cuadro.get_rect(), border_radius=18)
                    pygame.draw.rect(cuadro, (0, 0, 0), cuadro.get_rect(), 5, border_radius=18)
                    self.pantalla.blit(cuadro, (x - 130, y))

                    # Medalla
                    medalla = pygame.transform.scale(medallas[i], tamanios_medalla[i])
                    self.pantalla.blit(medalla, (x - tamanios_medalla[i][0] // 2, y - 160))

                    # Nombre y puntaje
                    self.dibujar_texto_con_sombra(str(nombre), self.fuente_nombre,
                                                  self.color_nombre, x, y + 45, centro=True)
                    self.dibujar_texto_con_sombra(f"{puntaje} pts", self.fuente_puntaje,
                                                  self.color_puntaje, x, y + 95, centro=True)

            # --- Botón Volver colorido ---
            # MODIFICADO: Siempre seleccionado con colores vibrantes
            color = self.color_boton_hover  # Naranja vibrante

            pygame.draw.rect(self.pantalla, color, boton_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, (255, 255, 255), boton_rect, 3, border_radius=20)  # Borde blanco

            self.dibujar_texto_con_sombra(self.txt["volver"], self.fuente_boton,
                                          (255, 255, 255), boton_rect.centerx, boton_rect.centery, centro=True)

            # ----------------------------------------------------
            # ⬇️ BLOQUE DE LECTURA SERIAL (AÑADIDO) ⬇️
            # ----------------------------------------------------
            if self.arduino_serial is not None and self.arduino_serial.is_open:
                try:
                    while self.arduino_serial.in_waiting > 0:
                        linea = self.arduino_serial.readline().decode('utf-8').strip()
                        
                        evento_tipo = None
                        evento_key = None

                        # Solo nos importa K_LEFT (D5) o K_RIGHT (D3) para volver
                        if linea == "LEFT_DOWN":
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

            # --- Eventos (MODIFICADOS) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.arduino_serial and self.arduino_serial.is_open:
                        self.arduino_serial.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    # MODIFICADO: K_LEFT (D5) o K_RIGHT (D3) te sacan
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_LEFT: # D5
                        return
                    elif event.key == pygame.K_RIGHT: # D3
                        return
                    elif event.key == pygame.K_RETURN:
                        return


            pygame.display.flip()
            clock.tick(60)

    def __del__(self):
        if self.conn:
            self.conn.close()