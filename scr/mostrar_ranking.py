import pygame
import mysql.connector
import sys
import serial # <-- MODIFICADO: Importado

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
                "titulo": "🏆 Top 3 Records",
                "no_records": "No hay récords todavía",
                "volver": "VOLVER"
            },
            "en": {
                "titulo": "🏆 Top 3 High Scores",
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

        # --- Colores ---
        self.color_titulo = (255, 255, 255)
        self.color_nombre = (255, 255, 255)
        self.color_puntaje = (255, 223, 0)
        self.color_sombra = (0, 0, 0)
        self.color_boton = (80, 80, 80)
        self.color_boton_hover = (200, 180, 50) # Este es el color "seleccionado"

        # --- Fondo e imágenes ---
        self.fondo = pygame.image.load("img/fondo.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ancho, alto))

        self.medalla_oro = pygame.image.load("img/oro.png").convert_alpha()
        self.medalla_plata = pygame.image.load("img/plata.png").convert_alpha()
        self.medalla_bronce = pygame.image.load("img/bronce.png").convert_alpha()

        # --- Conexión BD ---
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dino"
            )
            self.cursor = self.conn.cursor()
            print("[OK] Conectado a la base de datos MySQL")
        except mysql.connector.Error as e:
            print(f"[ERROR DB] No se pudo conectar: {e}")
            self.conn = None
            self.cursor = None

    def obtener_top3(self):
        if not self.cursor:
            return []
        try:
            self.cursor.execute("""
                SELECT u.Nombre, r.Puntaje
                FROM ranking r
                JOIN usuario u ON r.Id_Usuario = u.Id_Usuario
                ORDER BY r.Puntaje DESC
                LIMIT 3
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERROR SQL] {e}")
            return []

    def dibujar_texto_con_sombra(self, texto, fuente, color, x, y, centro=False):
        sombra = fuente.render(texto, True, self.color_sombra)
        render = fuente.render(texto, True, color)
        rect = render.get_rect(center=(x, y)) if centro else (x, y)
        sombra_rect = rect.copy()
        sombra_rect.move_ip(3, 3)
        self.pantalla.blit(sombra, sombra_rect)
        self.pantalla.blit(render, rect)

    def mostrar(self):
        clock = pygame.time.Clock()
        glow = 0
        glow_dir = 1
        boton_rect = pygame.Rect(self.ancho // 2 - 120, self.alto - 100, 240, 70)
        
        # En esta pantalla, el botón "Volver" está siempre seleccionado
        seleccionado = True 

        while True:
            # Fondo
            self.pantalla.blit(self.fondo, (0, 0))
            overlay = pygame.Surface((self.ancho, self.alto))
            overlay.set_alpha(130)
            overlay.fill((5, 5, 5))
            self.pantalla.blit(overlay, (0, 0))

            # Efecto glow en título
            glow += glow_dir * 3 
            if glow > 100 or glow < 0:
                glow_dir *= -1
            r = 255
            g = max(0, min(255, 255 - glow // 2))
            b = max(0, min(255, 255 - glow))
            color_brillo = (r, g, b)

            # --- Título principal ---
            self.dibujar_texto_con_sombra(self.txt["titulo"],
                                          self.fuente_titulo,
                                          color_brillo,
                                          self.ancho // 2, 90, centro=True)

            top3 = self.obtener_top3()

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

                    # Cuadro
                    cuadro = pygame.Surface((260, 130), pygame.SRCALPHA)
                    pygame.draw.rect(cuadro, (30, 30, 30, 220), cuadro.get_rect(), border_radius=18)
                    pygame.draw.rect(cuadro, (0, 0, 0), cuadro.get_rect(), 5, border_radius=18)
                    self.pantalla.blit(cuadro, (x - 130, y))

                    # Medalla
                    medalla = pygame.transform.scale(medallas[i], tamanios_medalla[i])
                    self.pantalla.blit(medalla, (x - tamanios_medalla[i][0] // 2, y - 160))

                    # Nombre y puntaje
                    self.dibujar_texto_con_sombra(nombre, self.fuente_nombre,
                                                  self.color_nombre, x, y + 45, centro=True)
                    self.dibujar_texto_con_sombra(f"{puntaje} pts", self.fuente_puntaje,
                                                  self.color_puntaje, x, y + 95, centro=True)

            # --- Botón Volver ---
            # MODIFICADO: Siempre seleccionado
            color = self.color_boton_hover

            pygame.draw.rect(self.pantalla, color, boton_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, (0, 0, 0), boton_rect, 3, border_radius=20)

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