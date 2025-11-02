import pygame
import mysql.connector
import sys

class MostrarRanking:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto

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
        self.color_boton_hover = (200, 180, 50)

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
        seleccionado = False

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
            self.dibujar_texto_con_sombra("🏆 Top 3 Records",
                                          self.fuente_titulo,
                                          color_brillo,
                                          self.ancho // 2, 90, centro=True)

            top3 = self.obtener_top3()

            if not top3:
                self.dibujar_texto_con_sombra("No hay récords todavía",
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
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hover = boton_rect.collidepoint(mouse_x, mouse_y)
            color = self.color_boton_hover if hover else self.color_boton

            pygame.draw.rect(self.pantalla, color, boton_rect, border_radius=20)
            pygame.draw.rect(self.pantalla, (0, 0, 0), boton_rect, 3, border_radius=20)

            self.dibujar_texto_con_sombra("VOLVER", self.fuente_boton,
                                          (255, 255, 255), boton_rect.centerx, boton_rect.centery, centro=True)

            # --- Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_RETURN and hover:
                        return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hover:
                        return

            pygame.display.flip()
            clock.tick(60)

    def __del__(self):
        if self.conn:
            self.conn.close()
