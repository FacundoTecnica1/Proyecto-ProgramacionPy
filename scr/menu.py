import pygame
import sys
import os
import serial # <-- MODIFICADO: Importado
from seleccionar_sonido import SelectorSonido
from mostrar_ranking import MostrarRanking

class Menu:
    # MODIFICADO: Añadido arduino_serial=None e idioma_inicial
    def __init__(self, pantalla, ancho, alto, record_actual, arduino_serial=None, idioma_inicial="es"):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.record_actual = record_actual
        self.arduino_serial = arduino_serial # <-- MODIFICADO

        # --- Idioma actual ---
        self.idioma = idioma_inicial # <-- MODIFICADO
        self.textos = {
            "es": {
                "titulo": "Dino",
                "record": "Record",
                "jugador": "Jugador",
                "opciones": ["Jugar", "Elegir Mundo", "Elegir Personaje", "Ver Rankings", "Salir"]
            },
            "en": {
                "titulo": "Dino Game",
                "record": "High Score",
                "jugador": "Player",
                "opciones": ["Play", "Choose World", "Choose Character", "View Rankings", "Exit"]
            }
        }
        self.actualizar_textos() # <-- MODIFICADO

        # MODIFICADO: Empezar en "Jugar" (índice 1)
        self.opcion_seleccionada = 1  # 0 = config superior, 1 = Jugar, ...
        self.seleccion_horizontal = 0  # 0 = idioma, 1 = música

        # Colores y fuentes
        self.color_texto = (255, 255, 255)
        self.color_hover = (255, 230, 150)
        self.color_sombra = (0, 0, 0, 120)
        self.color_boton = (50, 50, 50)
        self.radio_boton = 20
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_opcion = pygame.font.Font(None, 55)
        self.fuente_record = pygame.font.Font(None, 40)
        self.fuente_idioma = pygame.font.Font(None, 35)

        self.volumen_sfx = 0.5

        # Fondo
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "img", "fondo.png")
        self.fondo_img = pygame.image.load(ruta_fondo).convert()
        self.fondo_img = pygame.transform.scale(self.fondo_img, (self.ancho, self.alto))

        # Icono de música
        ruta_icono = os.path.join(os.path.dirname(__file__), "..", "img", "IconoMusica.png")
        try:
            self.icono_musica = pygame.image.load(ruta_icono).convert_alpha()
            self.icono_musica = pygame.transform.scale(self.icono_musica, (60, 60))
        except Exception as e:
            print(f"No se pudo cargar IconoMusica: {e}")
            self.icono_musica = None

        # Posiciones
        self.rect_icono_musica = pygame.Rect(self.ancho - 80, 20, 60, 60)
        self.rect_boton_idioma = pygame.Rect(self.ancho - 250, 25, 150, 50)

        self.botones_rects = []
        self.nombre_actual = None
        self.id_usuario_actual = None

    # ------------------------------------------------------------
    # MODIFICADO: Nuevo método para actualizar todos los textos
    def actualizar_textos(self):
        self.txt = self.textos[self.idioma]
        self.opciones = self.txt["opciones"]

    # ------------------------------------------------------------
    def dibujar_boton(self, texto, x, y, seleccionado=False):
        ancho_boton, alto_boton = 350, 60
        rect = pygame.Rect(0, 0, ancho_boton, alto_boton)
        rect.center = (x, y)

        sombra_rect = rect.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4

        sombra_surf = pygame.Surface((ancho_boton, alto_boton), pygame.SRCALPHA)
        pygame.draw.rect(sombra_surf, self.color_sombra, sombra_surf.get_rect(), border_radius=self.radio_boton)
        self.pantalla.blit(sombra_surf, sombra_rect.topleft)

        color = self.color_hover if seleccionado else self.color_boton
        pygame.draw.rect(self.pantalla, color, rect, border_radius=self.radio_boton)

        texto_surf = self.fuente_opcion.render(texto, True, self.color_texto)
        texto_rect = texto_surf.get_rect(center=rect.center)
        self.pantalla.blit(texto_surf, texto_rect)

        return rect

    # ------------------------------------------------------------
    def dibujar_boton_idioma(self, seleccionado=False):
        color_borde = self.color_hover if seleccionado else (255, 255, 255)
        pygame.draw.rect(self.pantalla, (0, 0, 0), self.rect_boton_idioma, border_radius=25)
        pygame.draw.rect(self.pantalla, color_borde, self.rect_boton_idioma, 2, border_radius=25)

        # globo idioma
        centro_globo = (self.rect_boton_idioma.left + 20, self.rect_boton_idioma.centery)
        pygame.draw.circle(self.pantalla, color_borde, centro_globo, 9, 2)
        pygame.draw.line(self.pantalla, color_borde, (centro_globo[0] - 8, centro_globo[1]), (centro_globo[0] + 8, centro_globo[1]), 1)
        pygame.draw.line(self.pantalla, color_borde, (centro_globo[0], centro_globo[1] - 8), (centro_globo[0], centro_globo[1] + 8), 1)

        # CORREGIDO: Mostrar el idioma CONTRARIO (al que puedes cambiar)
        idioma_texto = "English" if self.idioma == "es" else "Español"
        texto_surf = self.fuente_idioma.render(idioma_texto, True, color_borde)
        self.pantalla.blit(texto_surf, (centro_globo[0] + 25, self.rect_boton_idioma.centery - 12))

    # ------------------------------------------------------------
    # MODIFICADO: Llama a actualizar_textos
    def cambiar_idioma(self):
        self.idioma = "en" if self.idioma == "es" else "es"
        self.actualizar_textos()

    # ------------------------------------------------------------
    def dibujar_icono_musica(self, seleccionado=False):
        if not self.icono_musica:
            return
        if seleccionado:
            pygame.draw.rect(self.pantalla, self.color_hover, self.rect_icono_musica.inflate(8, 8), 3, border_radius=10)
        self.pantalla.blit(self.icono_musica, self.rect_icono_musica.topleft)

    # ------------------------------------------------------------
    def mostrar(self):
        clock = pygame.time.Clock()
        total_opciones = len(self.opciones) + 1  # +1 por la barra superior (configuración)

        while True:
            self.pantalla.blit(self.fondo_img, (0, 0))

            # --- Título (MODIFICADO) ---
            titulo_surf = self.fuente_titulo.render(self.txt["titulo"], True, self.color_texto)
            titulo_rect = titulo_surf.get_rect(center=(self.ancho // 2, 100))
            self.pantalla.blit(titulo_surf, titulo_rect)

            # --- Info jugador (MODIFICADO) ---
            texto_record = f"{self.txt['record']}: {self.record_actual}"
            
            if self.nombre_actual:
                texto_jugador = f"{self.txt['jugador']}: {self.nombre_actual}"
                texto_completo = f"{texto_record}    |    {texto_jugador}"
            else:
                texto_completo = texto_record

            texto_surf = self.fuente_record.render(texto_completo, True, (230, 230, 230))
            texto_rect = texto_surf.get_rect(center=(self.ancho // 2, 165))
            self.pantalla.blit(texto_surf, texto_rect)
            pygame.draw.line(self.pantalla, (180, 180, 180),
                             (texto_rect.left - 10, texto_rect.bottom + 5),
                             (texto_rect.right + 10, texto_rect.bottom + 5), 2)

            # --- Dibujar configuración superior ---
            self.dibujar_boton_idioma(seleccionado=(self.opcion_seleccionada == 0 and self.seleccion_horizontal == 0))
            self.dibujar_icono_musica(seleccionado=(self.opcion_seleccionada == 0 and self.seleccion_horizontal == 1))

            # --- Botones principales ---
            self.botones_rects.clear()
            espacio_vertical = 85 # MODIFICADO: Menos espacio para que quepan 5 opciones
            inicio_y = self.alto // 2 - 120 # MODIFICADO: Subir un poco
            x_centro = self.ancho // 2

            # MODIFICADO: Itera sobre self.opciones (que ahora se actualiza)
            for i, opcion in enumerate(self.opciones):
                indice_real = i + 1
                y = inicio_y + i * espacio_vertical
                rect = self.dibujar_boton(opcion, x_centro, y,
                                          seleccionado=(self.opcion_seleccionada == indice_real))
                self.botones_rects.append(rect)

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
                            # Solo nos interesan los KEYDOWN para menús
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


            # --- Controles (MODIFICADOS) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.arduino_serial and self.arduino_serial.is_open:
                        self.arduino_serial.close()
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: # D2
                        if self.opcion_seleccionada == 0 and self.seleccion_horizontal == 0:
                            self.cambiar_idioma() # Cambiar idioma con UP
                        else:
                            self.opcion_seleccionada = (self.opcion_seleccionada - 1) % total_opciones

                    elif event.key == pygame.K_DOWN: # D4
                        if self.opcion_seleccionada == 0 and self.seleccion_horizontal == 0:
                            self.cambiar_idioma() # Cambiar idioma con DOWN
                        else:
                            self.opcion_seleccionada = (self.opcion_seleccionada + 1) % total_opciones

                    elif event.key == pygame.K_LEFT: # D5
                         if self.opcion_seleccionada == 0:
                            self.seleccion_horizontal = (self.seleccion_horizontal - 1) % 2
                         # MODIFICADO: Si se presiona IZQUIERDA en un botón, no hace nada.
                         # else:
                         #    No hacer nada (no salir del juego)


                    elif event.key == pygame.K_RIGHT: # D3
                        if self.opcion_seleccionada == 0:
                            # Barra de configuración
                            if self.seleccion_horizontal == 0:
                                self.seleccion_horizontal = 1 # Mover a Música
                            elif self.seleccion_horizontal == 1:
                                # MODIFICADO: Pasa el arduino_serial y el idioma
                                selector = SelectorSonido(self.pantalla, self.ancho, self.alto, self.volumen_sfx, self.arduino_serial, self.idioma)
                                self.volumen_sfx = selector.mostrar()
                        else:
                            # Confirmar botón principal con DERECHA (D3)
                            # MODIFICADO: usa self.opciones que ya está traducido
                            seleccion = self.opciones[self.opcion_seleccionada - 1]
                            
                            # Compara con las claves en inglés (que no cambian)
                            clave_en = self.textos["en"]["opciones"][self.opcion_seleccionada - 1]

                            if clave_en == "Play":
                                return "jugar"
                            elif clave_en == "Choose World":
                                return "mundo"
                            elif clave_en == "Choose Character":
                                return "personaje"
                            elif clave_en == "View Rankings":
                                # MODIFICADO: Pasa el arduino_serial y el idioma
                                pantalla_ranking = MostrarRanking(self.pantalla, self.ancho, self.alto, self.arduino_serial, self.idioma)
                                pantalla_ranking.mostrar()
                            elif clave_en == "Exit":
                                return "salir" # Devuelve "salir" para que main.py lo maneje

            pygame.display.flip()
            clock.tick(60)