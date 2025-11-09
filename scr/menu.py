import pygame
import sys
import os
import math  # <-- AÑADIDO para las transiciones
import random  # <-- AÑADIDO para efectos de partículas
import serial # <-- MODIFICADO: Importado
from mostrar_ranking import MostrarRanking
from transiciones import TransicionPantalla, capturar_pantalla  # <-- NUEVO: Para transiciones épicas

# --- FUNCIONES DE MÚSICA DEL MENÚ ---
def cargar_musica_menu():
    """Carga la música del menú"""
    try:
        pygame.mixer.music.load(os.path.join("musica", "MenuMusica.mp3"))
        pygame.mixer.music.set_volume(0.4)  # Volumen al 40% para el menú
        print("[MÚSICA MENÚ] Música del menú cargada correctamente")
        return True
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo cargar la música del menú: {e}")
        return False
    try:
        pygame.mixer.music.set_volume(0.0)
        print("[MÚSICA MENÚ] Música muteada")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo mutear la música: {e}")

def desmutear_musica_menu(volumen):
    """Desmutea la música del menú"""
    try:
        volumen_musica = volumen * 0.4  # Restaurar volumen proporcional
        pygame.mixer.music.set_volume(volumen_musica)
        print(f"[MÚSICA MENÚ] Música desmuteada, volumen: {volumen_musica:.2f}")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo desmutear la música: {e}")

def iniciar_musica_menu():
    """Inicia la música del menú en loop"""
    try:
        pygame.mixer.music.play(-1)  # -1 significa loop infinito
        print("[MÚSICA MENÚ] Música del menú iniciada")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo iniciar la música del menú: {e}")

def detener_musica_menu():
    """Detiene la música del menú"""
    try:
        pygame.mixer.music.stop()
        print("[MÚSICA MENÚ] Música del menú detenida")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo detener la música del menú: {e}")

def pausar_musica_menu():
    """Pausa la música del menú"""
    try:
        pygame.mixer.music.pause()
        print("[MÚSICA MENÚ] Música del menú pausada")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo pausar la música del menú: {e}")

def reanudar_musica_menu():
    """Reanuda la música del menú de forma inteligente"""
    try:
        if pygame.mixer.music.get_busy():
            # Si ya hay música, solo unpause por si estaba pausada
            pygame.mixer.music.unpause()
            print("[MÚSICA MENÚ] Música reanudada (unpause)")
        else:
            # Si no hay música, necesitamos recargar e iniciar
            cargar_musica_menu()
            iniciar_musica_menu()
            print("[MÚSICA MENÚ] Música reiniciada desde cero")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo reanudar la música del menú: {e}")

def iniciar_musica_menu_suave():
    """Inicia la música del menú solo si no está ya reproduciéndose"""
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # -1 significa loop infinito
            print("[MÚSICA MENÚ] Música del menú iniciada")
        else:
            print("[MÚSICA MENÚ] Música ya reproduciéndose, no interrumpir")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo iniciar la música del menú: {e}")

def reanudar_musica_menu_original():
    """Reanuda la música del menú (función original)"""
    try:
        pygame.mixer.music.unpause()
        print("[MÚSICA MENÚ] Música del menú reanudada")
    except Exception as e:
        print(f"[ERROR MÚSICA MENÚ] No se pudo reanudar la música del menú: {e}")

class Menu:
    # MODIFICADO: Añadido arduino_serial=None e idioma_inicial
    def __init__(self, pantalla, ancho, alto, record_actual, arduino_serial=None, idioma_inicial="es"):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.record_actual = record_actual
        self.arduino_serial = arduino_serial # <-- MODIFICADO

        # --- MÚSICA DEL MENÚ ---
        self.musica_cargada = cargar_musica_menu()
        if self.musica_cargada:
            iniciar_musica_menu()

        # --- Idioma actual ---
        self.idioma = idioma_inicial # <-- MODIFICADO
        self.textos = {
            "es": {
                "titulo": "Dino",
                "record": "Record",
                "jugador": "Jugador",
                "opciones": ["1. Jugar", "2. Elegir Mundo", "3. Elegir Personaje", "4. Ver Rankings", "5. Salir"]
            },
            "en": {
                "titulo": "Dino Game",
                "record": "High Score",
                "jugador": "Player",
                "opciones": ["1. Play", "2. Choose World", "3. Choose Character", "4. View Rankings", "5. Exit"]
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
        self.muted = False
        self.volumen_anterior = self.volumen_sfx

        # --- VARIABLES DE TRANSICIÓN SUAVE ---
        self.transicion_activa = False
        self.tiempo_transicion = 0
        self.duracion_transicion = 200  # milisegundos
        self.opcion_anterior = self.opcion_seleccionada
        self.seleccion_horizontal_anterior = self.seleccion_horizontal
        self.alpha_transicion = 255  # opacidad de la transición

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

        # Color del botón con efectos especiales si está seleccionado
        if seleccionado:
            # Efecto de brillo pulsante
            tiempo_actual = pygame.time.get_ticks()
            brillo = abs(math.sin(tiempo_actual * 0.005)) * 50 + 50  # Pulso entre 50-100
            color = (int(50 + brillo), int(50 + brillo), int(50 + brillo * 0.5))
            
            # Borde brillante
            pygame.draw.rect(self.pantalla, self.color_hover, rect, 3, border_radius=self.radio_boton)
            
            # Efectos de partículas en las esquinas (solo algunas veces)
            if random.random() < 0.3:  # 30% de probabilidad cada frame
                for i in range(4):
                    corner_x = rect.left if i < 2 else rect.right
                    corner_y = rect.top if i % 2 == 0 else rect.bottom
                    offset_x = random.randint(-8, 8)
                    offset_y = random.randint(-8, 8)
                    pygame.draw.circle(self.pantalla, (255, 255, 100), 
                                     (corner_x + offset_x, corner_y + offset_y), 2)
        else:
            color = self.color_boton

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
    def iniciar_transicion(self):
        """Inicia una transición suave entre selecciones"""
        self.transicion_activa = True
        self.tiempo_transicion = pygame.time.get_ticks()
        self.opcion_anterior = self.opcion_seleccionada
        self.seleccion_horizontal_anterior = self.seleccion_horizontal
        self.alpha_transicion = 255

    def actualizar_transicion(self):
        """Actualiza el estado de la transición"""
        if not self.transicion_activa:
            return
        
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_transicion
        
        if tiempo_transcurrido >= self.duracion_transicion:
            self.transicion_activa = False
            self.alpha_transicion = 255
        else:
            # Interpolación suave (ease-out)
            progreso = tiempo_transcurrido / self.duracion_transicion
            self.alpha_transicion = int(255 * (1 - progreso * progreso))

    def dibujar_efecto_transicion(self):
        """Dibuja efectos visuales durante la transición"""
        if not self.transicion_activa:
            return
            
        # Crear superficie de transición con transparencia
        superficie_transicion = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        
        # Efecto de ondas desde el centro
        centro_x, centro_y = self.ancho // 2, self.alto // 2
        radio_max = 150
        
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_transicion
        progreso = min(tiempo_transcurrido / self.duracion_transicion, 1.0)
        
        # Ondas concéntricas
        for i in range(3):
            radio = int(radio_max * progreso - i * 30)
            if radio > 0:
                alpha = max(0, self.alpha_transicion - i * 60)
                color_onda = (255, 230, 150, alpha // 3)
                pygame.draw.circle(superficie_transicion, color_onda, 
                                 (centro_x, centro_y), radio, 3)
        
        # Partículas brillantes
        for i in range(8):
            angulo = (tiempo_transcurrido * 0.01 + i * 45) % 360
            radio_particula = 80 + 30 * progreso
            x = centro_x + radio_particula * math.cos(math.radians(angulo))
            y = centro_y + radio_particula * math.sin(math.radians(angulo))
            
            alpha_particula = max(0, self.alpha_transicion - 100)
            color_particula = (255, 255, 100, alpha_particula)
            pygame.draw.circle(superficie_transicion, color_particula, 
                             (int(x), int(y)), 4)
        
        self.pantalla.blit(superficie_transicion, (0, 0))

    # ------------------------------------------------------------
    def dibujar_icono_musica(self, seleccionado=False):
        if not self.icono_musica:
            return
        if seleccionado:
            pygame.draw.rect(self.pantalla, self.color_hover, self.rect_icono_musica.inflate(8, 8), 3, border_radius=10)
        self.pantalla.blit(self.icono_musica, self.rect_icono_musica.topleft)
        
        # Dibujar línea de mute si el sonido está muteado
        if self.muted:
            start_pos = (self.rect_icono_musica.left + 10, self.rect_icono_musica.bottom - 10)
            end_pos = (self.rect_icono_musica.right - 10, self.rect_icono_musica.top + 10)
            # Dibujar primero una línea negra más gruesa para cubrir cualquier trazo rojo del icono,
            # luego dibujar la línea amarilla encima para que se vea claramente amarilla.
            pygame.draw.line(self.pantalla, (0, 0, 0), start_pos, end_pos, 7)
            pygame.draw.line(self.pantalla, (255, 215, 100), start_pos, end_pos, 5)

    # ------------------------------------------------------------
    def mostrar(self):
        clock = pygame.time.Clock()
        total_opciones = len(self.opciones) + 1  # +1 por la barra superior (configuración)

        while True:
            # --- VERIFICAR CONTINUIDAD DE MÚSICA ---
            self.verificar_musica_continua()
            
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

            # --- Botones principales en 2 columnas ---
            # Layout: primeras 4 opciones en 2 columnas x 2 filas, la última opción (Salir) centrada abajo
            self.botones_rects.clear()
            x_centro = self.ancho // 2
            columna_offset = 220  # separación horizontal entre columnas
            inicio_y = self.alto // 2 - 70
            espacio_vertical = 120

            # Dibujar las primeras 4 opciones en 2 columnas
            for i in range(min(4, len(self.opciones))):
                opcion = self.opciones[i]
                indice_real = i + 1
                fila = i // 2  # 0 o 1
                col = i % 2    # 0 = izquierda, 1 = derecha
                x = x_centro - columna_offset if col == 0 else x_centro + columna_offset
                y = inicio_y + fila * espacio_vertical
                rect = self.dibujar_boton(opcion, x, y,
                                          seleccionado=(self.opcion_seleccionada == indice_real))
                self.botones_rects.append(rect)

            # Si hay una quinta opción (Salir), dibujarla centrada un poco más abajo
            if len(self.opciones) >= 5:
                opcion_salir = self.opciones[4]
                indice_salir = 5
                y_salir = inicio_y + 2 * espacio_vertical + 20
                rect_salir = self.dibujar_boton(opcion_salir, x_centro, y_salir,
                                                seleccionado=(self.opcion_seleccionada == indice_salir))
                self.botones_rects.append(rect_salir)

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
                            self.iniciar_transicion()  # Activar transición
                        else:
                            self.iniciar_transicion()  # Activar transición
                            self.opcion_seleccionada = (self.opcion_seleccionada - 1) % total_opciones

                    elif event.key == pygame.K_DOWN: # D4
                        if self.opcion_seleccionada == 0 and self.seleccion_horizontal == 0:
                            self.cambiar_idioma() # Cambiar idioma con DOWN
                            self.iniciar_transicion()  # Activar transición
                        else:
                            self.iniciar_transicion()  # Activar transición
                            self.opcion_seleccionada = (self.opcion_seleccionada + 1) % total_opciones

                    elif event.key == pygame.K_LEFT: # D5
                         if self.opcion_seleccionada == 0:
                            self.iniciar_transicion()  # Activar transición
                            self.seleccion_horizontal = (self.seleccion_horizontal - 1) % 2
                         # MODIFICADO: Si se presiona IZQUIERDA en un botón, no hace nada.
                         # else:
                         #    No hacer nada (no salir del juego)


                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_RETURN: # D3 o Enter
                        if self.opcion_seleccionada == 0:
                            if self.seleccion_horizontal == 0:
                                self.seleccion_horizontal = 1 # Mover a Música
                            elif self.seleccion_horizontal == 1:
                                # Toggle mute/unmute
                                if self.muted:
                                    self.muted = False
                                    self.volumen_sfx = self.volumen_anterior
                                    # Desmutear también la música
                                    if self.musica_cargada:
                                        desmutear_musica_menu(self.volumen_sfx)
                                else:
                                    self.muted = True
                                    self.volumen_anterior = self.volumen_sfx
                                    self.volumen_sfx = 0
                                    # Mutear también la música
                                    if self.musica_cargada:
                                        pygame.mixer.music.set_volume(0)
                        else:
                            # Confirmar botón principal con DERECHA (D3)
                            # MODIFICADO: Quitamos los números del inicio para la comparación
                            seleccion = self.opciones[self.opcion_seleccionada - 1]
                            
                            # Quita el número y el punto del inicio (ej: "1. Play" -> "Play")
                            opcion_limpia = seleccion[3:]  # Saltamos "X. "
                            
                            if opcion_limpia.startswith(("Jugar", "Play")):
                                # Pausar música del menú SOLO al ir a jugar
                                if self.musica_cargada:
                                    pausar_musica_menu()
                                return "jugar"
                            elif opcion_limpia.startswith(("Elegir Mundo", "Choose World")):
                                # NO pausar música - mantener continua en submenús
                                return "mundo"
                            elif opcion_limpia.startswith(("Elegir Personaje", "Choose Character")):
                                # NO pausar música - mantener continua en submenús
                                return "personaje"
                            elif opcion_limpia.startswith(("Ver Rankings", "View Rankings")):
                                # CAPTURAR PANTALLA ACTUAL PARA TRANSICIÓN ÉPICA
                                superficie_menu = capturar_pantalla(self.pantalla)
                                
                                # CREAR TRANSICIÓN ZOOM SPIRAL PARA RANKING
                                transicion = TransicionPantalla(self.pantalla, self.ancho, self.alto)
                                
                                # CREAR SUPERFICIE CON EFECTO ESPACIAL PARA RANKING
                                superficie_ranking = pygame.Surface((self.ancho, self.alto))
                                superficie_ranking.fill((80, 50, 20))  # Dorado/naranja para ranking
                                # Añadir estrellas doradas y trofeos
                                for i in range(60):
                                    x = random.randint(0, self.ancho)
                                    y = random.randint(0, self.alto)
                                    color_estrella = random.choice([(255, 215, 0), (255, 255, 100), (255, 200, 50)])
                                    pygame.draw.circle(superficie_ranking, color_estrella, (x, y), random.randint(1, 4))
                                
                                # Añadir texto épico para ranking
                                fuente_ranking = pygame.font.Font(None, 60)
                                if self.idioma == "es":
                                    texto_ranking = fuente_ranking.render("SALÓN DE LA FAMA...", True, (255, 215, 0))
                                else:
                                    texto_ranking = fuente_ranking.render("HALL OF FAME...", True, (255, 215, 0))
                                texto_rect = texto_ranking.get_rect(center=(self.ancho//2, self.alto//2))
                                superficie_ranking.blit(texto_ranking, texto_rect)
                                
                                # ZOOM SPIRAL ÉPICO PARA RANKING
                                transicion.transicion_zoom_spiral(superficie_menu, superficie_ranking, 700)
                                
                                # MOSTRAR RANKING NORMALMENTE
                                pantalla_ranking = MostrarRanking(self.pantalla, self.ancho, self.alto, self.arduino_serial, self.idioma)
                                pantalla_ranking.mostrar()
                                
                                # TRANSICIÓN DE REGRESO ÉPICA
                                superficie_ranking_salida = capturar_pantalla(self.pantalla)
                                
                                # Renderizar menú de regreso
                                superficie_menu_regreso = pygame.Surface((self.ancho, self.alto))
                                superficie_menu_regreso.blit(self.fondo_img, (0, 0))
                                titulo_surf = self.fuente_titulo.render(self.txt["titulo"], True, self.color_texto)
                                titulo_rect = titulo_surf.get_rect(center=(self.ancho // 2, 100))
                                superficie_menu_regreso.blit(titulo_surf, titulo_rect)
                                
                                # ZOOM SPIRAL INVERSO ÉPICO
                                transicion.transicion_zoom_spiral(superficie_ranking_salida, superficie_menu_regreso, 600)
                            elif opcion_limpia.startswith(("Salir", "Exit")):
                                # Detener música antes de salir
                                if self.musica_cargada:
                                    detener_musica_menu()
                                return "salir" # Devuelve "salir" para que main.py lo maneje
                    
                    # --- CONTROLES DE VOLUMEN ADICIONALES ---
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Tecla + (aumentar volumen)
                        if not self.muted and self.volumen_sfx < 1.0:
                            self.volumen_sfx = min(1.0, self.volumen_sfx + 0.1)
                            self.actualizar_volumen_total()
                            print(f"[VOLUMEN] Volumen aumentado a {self.volumen_sfx:.1f}")
                    
                    elif event.key == pygame.K_MINUS:  # Tecla - (disminuir volumen)
                        if not self.muted and self.volumen_sfx > 0.0:
                            self.volumen_sfx = max(0.0, self.volumen_sfx - 0.1)
                            self.actualizar_volumen_total()
                            print(f"[VOLUMEN] Volumen disminuido a {self.volumen_sfx:.1f}")
                    
                    elif event.key == pygame.K_m:  # Tecla M (mute/unmute rápido)
                        if self.muted:
                            self.muted = False
                            self.volumen_sfx = self.volumen_anterior
                            if self.musica_cargada:
                                desmutear_musica_menu(self.volumen_sfx)
                            print("[VOLUMEN] Audio desmuteado")
                        else:
                            self.muted = True
                            self.volumen_anterior = self.volumen_sfx
                            self.volumen_sfx = 0
                            if self.musica_cargada:
                                pygame.mixer.music.set_volume(0)
                            print("[VOLUMEN] Audio muteado")

            # --- ACTUALIZAR Y DIBUJAR TRANSICIONES ---
            self.actualizar_transicion()
            self.dibujar_efecto_transicion()

            pygame.display.flip()
            clock.tick(60)
    
    def actualizar_volumen_total(self):
        """Actualiza tanto el volumen de efectos como el de música"""
        if self.musica_cargada:
            if self.muted:
                pygame.mixer.music.set_volume(0)
            else:
                # Volumen de música al 40% del volumen de efectos
                pygame.mixer.music.set_volume(self.volumen_sfx * 0.4)

    def verificar_musica_continua(self):
        """Verifica que la música del menú siga reproduciéndose continuamente"""
        if self.musica_cargada and not pygame.mixer.music.get_busy():
            print("[MÚSICA MENÚ] Música interrumpida, reiniciando...")
            cargar_musica_menu()
            iniciar_musica_menu()
            # Restaurar volumen después de reiniciar
            self.actualizar_volumen_total()
    
    def detener_musica(self):
        """Método para detener la música del menú desde fuera de la clase"""
        if self.musica_cargada:
            detener_musica_menu()
    
    def pausar_musica(self):
        """Método para pausar la música del menú"""
        if self.musica_cargada:
            pausar_musica_menu()
    
    def reanudar_musica(self):
        """Método para reanudar la música del menú (solo si está pausada)"""
        if self.musica_cargada:
            print("[MÚSICA MENÚ] Verificando estado de música del menú...")
            try:
                # Solo actuar si la música NO está reproduciéndose
                if not pygame.mixer.music.get_busy():
                    print("[MÚSICA MENÚ] Música no activa, recargando...")
                    # Si no hay música reproduciéndose, recargar e iniciar
                    cargar_musica_menu()
                    iniciar_musica_menu()
                else:
                    print("[MÚSICA MENÚ] Música ya reproduciéndose, no interrumpir")
                    # Si ya está reproduciéndose, no hacer nada para mantener continuidad
            except Exception as e:
                print(f"[ERROR] Problema al verificar música del menú: {e}")
                # Intentar cargar de nuevo como fallback solo si es necesario
                if not pygame.mixer.music.get_busy():
                    cargar_musica_menu()
                    iniciar_musica_menu()