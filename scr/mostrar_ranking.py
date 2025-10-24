import pygame
import mysql.connector
import sys

class MostrarRanking:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto

        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_texto = pygame.font.Font(None, 50)
        self.fuente_info = pygame.font.Font(None, 40)

        self.color_fondo = (15, 20, 30)
        self.color_texto = (255, 255, 255)

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

    def mostrar(self):
        clock = pygame.time.Clock()
        while True:
            self.pantalla.fill(self.color_fondo)

            titulo = self.fuente_titulo.render("🏆 RANKING TOP 3 🏆", True, self.color_texto)
            self.pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 80)))

            top3 = self.obtener_top3()
            y = 200
            medallas = ["🥇", "🥈", "🥉"]

            if not top3:
                msg = self.fuente_info.render("No hay récords todavía.", True, (200, 200, 200))
                self.pantalla.blit(msg, msg.get_rect(center=(self.ancho // 2, self.alto // 2)))
            else:
                for i, (nombre, puntaje) in enumerate(top3):
                    texto = f"{medallas[i]} {nombre} — {puntaje} pts"
                    render = self.fuente_texto.render(texto, True, self.color_texto)
                    self.pantalla.blit(render, render.get_rect(center=(self.ancho // 2, y)))
                    y += 90

            volver = self.fuente_info.render("Presioná ESC para volver", True, (180, 180, 180))
            self.pantalla.blit(volver, volver.get_rect(center=(self.ancho // 2, self.alto - 50)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            pygame.display.flip()
            clock.tick(60)

    def __del__(self):
        if self.conn:
            self.conn.close()
