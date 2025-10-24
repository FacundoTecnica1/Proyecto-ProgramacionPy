import pygame
import sys
import os
import mysql.connector

class ElegirNombre:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto

        # 🎨 Estilo visual
        self.color_texto = (255, 255, 255)
        self.color_resaltado = (255, 215, 100)
        self.color_fondo = (25, 25, 35)
        self.fuente_titulo = pygame.font.Font(None, 100)
        self.fuente_letra = pygame.font.Font(None, 120)
        self.fuente_info = pygame.font.Font(None, 40)

        # 🖼️ Fondo opcional
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
        if os.path.exists(ruta_fondo):
            self.fondo_img = pygame.image.load(ruta_fondo).convert()
            self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))
        else:
            self.fondo_img = None

        # 🔤 Letras y estado
        self.letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.indice = [0, 0, 0, 0]
        self.posicion_actual = 0

        # ⚙️ Base de datos
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
    # 📦 BASE DE DATOS
    # ============================
    def crear_tablas(self):
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

    def guardar_nombre(self, nombre):
        """Guarda el nombre en la base de datos y devuelve su ID"""
        conexion = mysql.connector.connect(**self.db_config)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuario (Nombre) VALUES (%s);", (nombre,))
        conexion.commit()
        self.id_usuario_actual = cursor.lastrowid
        conexion.close()
        print(f"[INFO] Usuario '{nombre}' guardado con ID {self.id_usuario_actual}")
        return self.id_usuario_actual

    def obtener_nombre_guardado(self):
        conexion = mysql.connector.connect(**self.db_config)
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre FROM usuario ORDER BY Id_Usuario DESC LIMIT 1;")
        fila = cursor.fetchone()
        conexion.close()
        return fila[0] if fila else None

    # ============================
    # 🔠 INTERFAZ
    # ============================
    def cargar_nombre_guardado(self, nombre):
        nombre = nombre.upper()[:4]
        for i, letra in enumerate(nombre):
            if letra in self.letras:
                self.indice[i] = self.letras.index(letra)

    def mostrar(self):
        clock = pygame.time.Clock()

        while True:
            if self.fondo_img:
                self.pantalla.blit(self.fondo_img, (0, 0))
            else:
                self.pantalla.fill(self.color_fondo)

            titulo_texto = "ELIGE TU NOMBRE"
            sombra = self.fuente_titulo.render(titulo_texto, True, (0, 0, 0))
            texto = self.fuente_titulo.render(titulo_texto, True, self.color_texto)
            rect = texto.get_rect(center=(self.ancho // 2, 120))
            self.pantalla.blit(sombra, (rect.x + 3, rect.y + 3))
            self.pantalla.blit(texto, rect)

            inicio_x = self.ancho // 2 - 1.5 * 140
            for i in range(4):
                letra = self.letras[self.indice[i]]
                color = self.color_resaltado if i == self.posicion_actual else self.color_texto
                surf = self.fuente_letra.render(letra, True, color)
                rect = surf.get_rect(center=(inicio_x + i * 140, self.alto // 2))
                self.pantalla.blit(surf, rect)
                if i == self.posicion_actual:
                    pygame.draw.rect(self.pantalla, self.color_resaltado,
                                     rect.inflate(30, 30), 3, border_radius=15)

            info_text = "↑ ↓ Cambiar letra   ← → Mover   ENTER Confirmar"
            info = self.fuente_info.render(info_text, True, (200, 200, 200))
            self.pantalla.blit(info, info.get_rect(center=(self.ancho // 2, self.alto - 80)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.indice[self.posicion_actual] = (self.indice[self.posicion_actual] + 1) % len(self.letras)
                    elif event.key == pygame.K_DOWN:
                        self.indice[self.posicion_actual] = (self.indice[self.posicion_actual] - 1) % len(self.letras)
                    elif event.key == pygame.K_RIGHT:
                        self.posicion_actual = (self.posicion_actual + 1) % 4
                    elif event.key == pygame.K_LEFT:
                        self.posicion_actual = (self.posicion_actual - 1) % 4
                    elif event.key == pygame.K_RETURN:
                        nombre = "".join([self.letras[i] for i in self.indice])
                        id_usuario = self.guardar_nombre(nombre)
                        return nombre, id_usuario

            pygame.display.flip()
            clock.tick(60)
