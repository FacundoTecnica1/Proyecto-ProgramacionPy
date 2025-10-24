import pygame
import sys
import os
import mysql.connector

class MostrarRanking:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_texto = pygame.font.Font(None, 60)
        self.fuente_volver = pygame.font.Font(None, 40)
        self.color_texto = (255, 255, 255)

        # 🎨 Fondo
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
        if os.path.exists(ruta_fondo):
            self.fondo_img = pygame.image.load(ruta_fondo).convert()
            self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))
        else:
            self.fondo_img = None

        # ⚙️ Config DB
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "dino"
        }

        # Crear tablas si no existen
        self.crear_tablas_si_no_existen()

    # =============================
    # 🗄️ BASE DE DATOS
    # =============================
    def crear_tablas_si_no_existen(self):
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

    def obtener_top3(self):
        conexion = mysql.connector.connect(**self.db_config)
        cursor = conexion.cursor()

        # 🔝 Obtener los 3 mejores jugadores
        cursor.execute("""
            SELECT u.Nombre, r.Puntaje
            FROM ranking r
            JOIN usuario u ON r.Id_Usuario = u.Id_Usuario
            ORDER BY r.Puntaje DESC
            LIMIT 3;
        """)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def guardar_o_actualizar_record(self, id_usuario, puntaje):
        """Guarda o actualiza el puntaje del jugador"""
        conexion = mysql.connector.connect(**self.db_config)
        cursor = conexion.cursor()

        cursor.execute("SELECT Puntaje FROM ranking WHERE Id_Usuario = %s;", (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            puntaje_actual = resultado[0]
            if puntaje > puntaje_actual:
                cursor.execute("UPDATE ranking SET Puntaje = %s WHERE Id_Usuario = %s;", (puntaje, id_usuario))
                print(f"[INFO] 🏆 Nuevo record para usuario {id_usuario}: {puntaje}")
        else:
            cursor.execute("INSERT INTO ranking (Id_Usuario, Puntaje) VALUES (%s, %s);", (id_usuario, puntaje))
            print(f"[INFO] Primer record guardado para usuario {id_usuario}: {puntaje}")

        conexion.commit()
        conexion.close()

    # =============================
    # 🎮 INTERFAZ VISUAL
    # =============================
    def mostrar(self):
        clock = pygame.time.Clock()
        top3 = self.obtener_top3()
        medallas = ["🥇", "🥈", "🥉"]

        while True:
            if self.fondo_img:
                self.pantalla.blit(self.fondo_img, (0, 0))
            else:
                self.pantalla.fill((30, 30, 40))

            # 🏆 Título
            titulo = self.fuente_titulo.render("🏆 TOP 3 JUGADORES 🏆", True, self.color_texto)
            self.pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 100)))

            # 👑 Mostrar jugadores
            y_base = 220
            if top3:
                for i, (nombre, puntaje) in enumerate(top3):
                    medalla = medallas[i]
                    texto = f"{medalla} {nombre}  -  {puntaje} pts"
                    surf = self.fuente_texto.render(texto, True, self.color_texto)
                    rect = surf.get_rect(center=(self.ancho // 2, y_base + i * 100))
                    self.pantalla.blit(surf, rect)
            else:
                sin_datos = self.fuente_texto.render("No hay puntajes aún 😔", True, (200, 200, 200))
                self.pantalla.blit(sin_datos, sin_datos.get_rect(center=(self.ancho // 2, self.alto // 2)))

            # 🔙 Texto para volver
            volver = self.fuente_volver.render("Presiona ESC para volver", True, (200, 200, 200))
            self.pantalla.blit(volver, volver.get_rect(center=(self.ancho // 2, self.alto - 80)))

            # 🎹 Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return  # volver al menú

            pygame.display.flip()
            clock.tick(60)
