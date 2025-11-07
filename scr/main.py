import pygame
import random
import sys
import os
import time  
import serial # <-- MODIFICADO: Importado
import mysql.connector # <-- MODIFICADO: Importado para guardar puntaje

# Importar todas las clases necesarias
from game_objects import Perro, Obstaculo, Fondo, Ave
from seleccion_personaje import SeleccionPersonaje
from utils import mostrar_texto
from menu import Menu
from seleccionar_mundo import SeleccionMundo
from elegir_nombre import ElegirNombre

pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 800, 700
FPS = 60
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dino")

# --- RUTA DE IMÁGENES (MOVIDA ARRIBA) ---
RUTA_BASE = os.path.join(os.path.dirname(__file__), "..", "img")

# ----------------------------------------------------
# ⬇️ CONFIGURACIÓN Y CONEXIÓN SERIAL (GLOBAL) ⬇️
# ----------------------------------------------------
# ⚠️ IMPORTANTE: CAMBIA 'COM4' por el puerto de tu Arduino
PUERTO_SERIAL = 'COM4' 
BAUD_RATE = 9600

arduino_serial = None
try:
    # timeout=0.1 permite que el programa no se bloquee esperando datos
    arduino_serial = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=0.1)
    time.sleep(2)  # Espera para que la conexión se establezca completamente
    print(f"[SERIAL] Conexión con Arduino establecida en {PUERTO_SERIAL}.")
except Exception as e:
    print(f"[ERROR SERIAL] No se pudo conectar a Arduino en {PUERTO_SERIAL}: {e}")
# ----------------------------------------------------
# ⬆️ FIN CONFIGURACIÓN SERIAL ⬆️
# ----------------------------------------------------

# --- FUENTES GLOBALES PARA PANTALLA INICIAL (NUEVO) ---
try:
    # Cambio a Arial como solicitado
    fuente_idioma_titulo = pygame.font.SysFont("arial", 80)
    fuente_idioma_opcion = pygame.font.SysFont("arial", 60)
    fuente_idioma_info = pygame.font.SysFont("arial", 36)
except Exception as e:
    print(f"Error al cargar fuentes: {e}")
    # Fallback a fuentes por defecto si Arial no está disponible
    fuente_idioma_titulo = pygame.font.Font(None, 80)
    fuente_idioma_opcion = pygame.font.Font(None, 60)
    fuente_idioma_info = pygame.font.Font(None, 36)

# --- FUNCIÓN DIBUJAR TEXTO (NUEVO) ---
def dibujar_texto_simple(pantalla, texto, fuente, color, x, y, centrado=True):
    """Función helper para dibujar texto centrado o alineado."""
    surf = fuente.render(texto, True, color)
    rect = surf.get_rect(center=(x, y)) if centrado else surf.get_rect(topleft=(x, y))
    pantalla.blit(surf, rect)

# --- FUNCIÓN DIBUJAR BOTÓN (NUEVO) ---
def dibujar_boton(pantalla, texto, fuente, color_texto, x, y, ancho=300, alto=80, seleccionado=False):
    """Dibuja un botón estilizado con bordes y efectos."""
    # Colores del botón
    if seleccionado:
        color_fondo = (80, 120, 200, 180)  # Azul translúcido cuando está seleccionado
        color_borde = (255, 230, 150)      # Borde dorado
        grosor_borde = 4
    else:
        color_fondo = (40, 40, 60, 150)    # Gris oscuro translúcido
        color_borde = (150, 150, 150)      # Borde gris
        grosor_borde = 2
    
    # Crear superficie para el botón con transparencia
    boton_rect = pygame.Rect(x - ancho//2, y - alto//2, ancho, alto)
    
    # Fondo del botón con transparencia
    boton_surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.rect(boton_surf, color_fondo, boton_surf.get_rect(), border_radius=15)
    pantalla.blit(boton_surf, boton_rect.topleft)
    
    # Borde del botón
    pygame.draw.rect(pantalla, color_borde, boton_rect, grosor_borde, border_radius=15)
    
    # Texto del botón
    texto_surf = fuente.render(texto, True, color_texto)
    texto_rect = texto_surf.get_rect(center=(x, y))
    pantalla.blit(texto_surf, texto_rect)
    
    return boton_rect

# --- FUNCIÓN SELECCIONAR IDIOMA (NUEVO) ---
def seleccionar_idioma_inicial(pantalla, ancho, alto):
    """Muestra la pantalla inicial de selección de idioma con botones estilizados."""
    global arduino_serial # Importante usar la global
    idioma_sel = "es"
    clock = pygame.time.Clock()
    
    try:
        ruta_fondo = os.path.join(RUTA_BASE, "fondo.png")
        fondo_img = pygame.image.load(ruta_fondo).convert()
        fondo_img = pygame.transform.scale(fondo_img, (ancho, alto))
    except Exception as e:
        print(f"Error al cargar fondo para selección de idioma: {e}")
        fondo_img = None

    while True:
        # Fondo
        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill((25, 25, 35))

        # Título principal
        dibujar_texto_simple(pantalla, "Seleccionar Idioma / Select Language", 
                             fuente_idioma_titulo, (255, 255, 255), ancho // 2, alto // 3)

        # Instrucciones
        dibujar_texto_simple(pantalla, "Usa las flechas para seleccionar / Use arrows to select", 
                             fuente_idioma_info, (200, 200, 200), ancho // 2, alto // 3 + 80)

        # Botones de idioma
        color_texto_es = (255, 255, 255) if idioma_sel == "es" else (200, 200, 200)
        color_texto_en = (255, 255, 255) if idioma_sel == "en" else (200, 200, 200)

        # Botón Español
        dibujar_boton(pantalla, "🇪🇸 Español", fuente_idioma_opcion, color_texto_es, 
                     ancho // 2 - 200, alto // 2 + 50, 280, 70, idioma_sel == "es")
        
        # Botón English  
        dibujar_boton(pantalla, "🇺🇸 English", fuente_idioma_opcion, color_texto_en, 
                     ancho // 2 + 200, alto // 2 + 50, 280, 70, idioma_sel == "en")

        # Instrucciones de confirmación
        dibujar_texto_simple(pantalla, "Presiona ARRIBA/ABAJO para confirmar / Press UP/DOWN to confirm", 
                             fuente_idioma_info, (180, 180, 180), ancho // 2, alto // 2 + 150)

        # --- Lectura Serial ---
        if arduino_serial is not None and arduino_serial.is_open:
            try:
                while arduino_serial.in_waiting > 0:
                    linea = arduino_serial.readline().decode('utf-8').strip()
                    evento_tipo = None
                    evento_key = None
                    if linea == "LEFT_DOWN": # D5
                        evento_tipo = pygame.KEYDOWN; evento_key = pygame.K_LEFT
                    elif linea == "RIGHT_DOWN": # D3
                        evento_tipo = pygame.KEYDOWN; evento_key = pygame.K_RIGHT
                    elif linea == "UP_DOWN": # D2 (Confirmar)
                        evento_tipo = pygame.KEYDOWN; evento_key = pygame.K_UP
                    elif linea == "DOWN_DOWN": # D4 (Confirmar)
                        evento_tipo = pygame.KEYDOWN; evento_key = pygame.K_DOWN
                    
                    if evento_tipo:
                        pygame.event.post(pygame.event.Event(evento_tipo, key=evento_key))
            except Exception as e:
                print(f"[ERROR SERIAL] {e}")
                try: arduino_serial.close()
                except: pass
                arduino_serial = None

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if arduino_serial and arduino_serial.is_open:
                    arduino_serial.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # D5
                    idioma_sel = "es"
                elif event.key == pygame.K_RIGHT: # D3
                    idioma_sel = "en"
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN: # D2 o D4
                    return idioma_sel
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return idioma_sel

        pygame.display.flip()
        clock.tick(60)

# --- SELECCIONAR IDIOMA ANTES DE NADA (NUEVO) ---
idioma_actual = seleccionar_idioma_inicial(VENTANA, ANCHO, ALTO)
print(f"Idioma seleccionado: {idioma_actual}")


# --- ELEGIR NOMBRE AL INICIO ---
# MODIFICADO: Se pasa el objeto arduino_serial y el idioma_actual
elegir_nombre = ElegirNombre(VENTANA, ANCHO, ALTO, arduino_serial, idioma_actual) 
nombre_jugador, id_usuario = elegir_nombre.mostrar()
print(f"Jugador: {nombre_jugador} (ID: {id_usuario})")


# --- COLORES ---
BLANCO = (255, 255, 255)
COLOR_ESPACIO_FONDO = (30, 30, 35)
ALTURA_SUELO = 30


# --- FUNCIÓN PARA CARGAR IMÁGENES ---
def cargar_imagen(nombre):
    return pygame.image.load(os.path.join(RUTA_BASE, nombre)).convert_alpha()

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

# --- CARGA BASE DE IMÁGENES (Se cargan todas ahora) ---
try:
    imagenes_base = {
        'perro_run': [
            cargar_imagen("perro_run1.png"),
            cargar_imagen("perro_run2.png"),
            cargar_imagen("perro_run3.png"),
            cargar_imagen("perro_run4.png")
        ],
        'perro_jump': cargar_imagen("perro_jump.png"),
        'perro_air': cargar_imagen("perro_air.png"),

        'gato_run': [
            cargar_imagen("gato_run1.png"),
            cargar_imagen("gato_run2.png"),
            cargar_imagen("gato_run3.png"),
            cargar_imagen("gato_run4.png")
        ],
        'gato_jump': cargar_imagen("gato_jump.png"),
        'gato_air': cargar_imagen("gato_air.png"),

        'cactus_noche': [
            cargar_imagen("cactus1.png"),
            cargar_imagen("cactus2.png"),
            cargar_imagen("cactus3.png")
        ],
        'cactus_dia': [
            cargar_imagen("cactus_verde1.png"),
            cargar_imagen("cactus_verde2.png"),
            cargar_imagen("cactus_verde3.png")
        ],
        'ave': [
            cargar_imagen("ave1.png"),
            cargar_imagen("ave2.png"),
            cargar_imagen("ave3.png")
        ],
        'fondo_noche': pygame.image.load(os.path.join(RUTA_BASE, "fondo.png")).convert(),
        'fondo_dia': pygame.image.load(os.path.join(RUTA_BASE, "fondo2.png")).convert(),
        'luna': cargar_imagen("luna.png"),
        'sol': cargar_imagen("sol.png"),
        'game_over': cargar_imagen("game_over.png")
    }
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    if arduino_serial and arduino_serial.is_open:
        arduino_serial.close()
    pygame.quit()
    sys.exit()

# --- ESCALAS ---
imagenes_base['fondo_noche'] = pygame.transform.scale(imagenes_base['fondo_noche'], (ANCHO, ALTO))
imagenes_base['fondo_dia'] = pygame.transform.scale(imagenes_base['fondo_dia'], (ANCHO, ALTO))
imagenes_base['luna'] = pygame.transform.scale(imagenes_base['luna'], (75, 75))
imagenes_base['sol'] = pygame.transform.scale(imagenes_base['sol'], (80, 80))

# Personajes
perro_run = [escalar_y_cuadrar(img, 150) for img in imagenes_base["perro_run"]]
gato_run = [escalar_y_cuadrar(img, 150) for img in imagenes_base["gato_run"]]
perro_jump = escalar_y_cuadrar(imagenes_base["perro_jump"], 150)
perro_air = escalar_y_cuadrar(imagenes_base["perro_air"], 150)
gato_jump = escalar_y_cuadrar(imagenes_base["gato_jump"], 150)
gato_air = escalar_y_cuadrar(imagenes_base["gato_air"], 150)
ave_imgs = escalar_lista(imagenes_base["ave"], 100, 80)

# Cactus (se escalarán dentro de bucle_juego)
cactus_noche_imgs = imagenes_base["cactus_noche"]
cactus_dia_imgs = imagenes_base["cactus_dia"]


# --- SONIDOS DE EFECTOS ---
sonido_salto = pygame.mixer.Sound(os.path.join("musica", "EfectoSonidoSalto.mp3"))
sonido_gameover = pygame.mixer.Sound(os.path.join("musica", "EfectoSonidoGameOver.mp3"))

def actualizar_volumen_sfx(volumen):
    sonido_salto.set_volume(volumen)
    sonido_gameover.set_volume(volumen)

# =================================================================
# ⬇️ NUEVA FUNCIÓN: BUCLE_JUEGO ⬇️
# =================================================================
def bucle_juego(personaje_elegido, mundo_elegido, nombre_jugador, id_jugador, volumen_sfx, record_previo):
    
    # ⬇️⬇️⬇️ ESTA ES LA LÍNEA AÑADIDA ⬇️⬇️⬇️
    global arduino_serial 
    # ⬆️⬆️⬆️ ESTA ES LA LÍNEA AÑADIDA ⬆️⬆️⬆️

    # --- Configurar entorno según selección ---
    if mundo_elegido == "dia":
        fondo_juego = imagenes_base['fondo_dia']
        astro_img = imagenes_base['sol']
        cactus_set = cactus_dia_imgs
    else: # noche
        fondo_juego = imagenes_base['fondo_noche']
        astro_img = imagenes_base['luna']
        cactus_set = cactus_noche_imgs

    # Escalar cactus
    cactus_imgs = escalar_lista(cactus_set, 110, 140)
    cactus_small = escalar_lista(cactus_set, 82, 105)


    # --- CREAR JUGADOR ---
    if personaje_elegido == "gato":
        jugador = Perro(gato_run, gato_jump, gato_air, ANCHO, ALTO, ALTURA_SUELO)
    else: # perro
        jugador = Perro(perro_run, perro_jump, perro_air, ANCHO, ALTO, ALTURA_SUELO)
    jugador.reiniciar(ALTO, ALTURA_SUELO)

    # --- OBJETOS DEL JUEGO ---
    fondo = Fondo(fondo_juego, 0.5)
    obstaculos = pygame.sprite.Group()
    aves = pygame.sprite.Group()

    puntaje = 0
    record = record_previo # Cargar el record anterior
    juego_activo = True
    velocidad_juego = 9.0 # AUMENTADO: Velocidad base más rápida (era 7.5)
    reloj = pygame.time.Clock()

    tiempo_ultimo_obstaculo = pygame.time.get_ticks()
    intervalo_cactus = random.randint(2000, 4000) # AUMENTADO: Más espaciados
    tiempo_ultima_ave = pygame.time.get_ticks()
    intervalo_ave = random.randint(5000, 9000)

    # --- Configuración de generación ---
    CHANCE_DOBLE_CACTUS = 0.15 # REDUCIDO: 15% de chance de que salgan 2 (era 30%)
    SEPARACION_MIN = 90 # AJUSTADO: Separación más corta pero esquivable
    SEPARACION_MAX = 140 # AJUSTADO: Máximo más razonable

    # --- Aplicar volumen ---
    actualizar_volumen_sfx(volumen_sfx)


    # --- BUCLE PRINCIPAL DEL JUEGO ---
    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS)
        
        # ----------------------------------------------------
        # ⬇️ BLOQUE DE LECTURA SERIAL (JUEGO) ⬇️
        # ----------------------------------------------------
        if arduino_serial is not None and arduino_serial.is_open:
            try:
                while arduino_serial.in_waiting > 0:
                    linea = arduino_serial.readline().decode('utf-8').strip()
                    
                    evento_tipo = None
                    evento_key = None

                    if linea == "UP_DOWN":
                        evento_tipo = pygame.KEYDOWN
                        evento_key = pygame.K_UP
                    elif linea == "UP_UP": # Necesario para soltar agacharse/flotar
                        evento_tipo = pygame.KEYUP
                        evento_key = pygame.K_UP
                    elif linea == "DOWN_DOWN": # Necesario para agacharse/flotar
                        evento_tipo = pygame.KEYDOWN
                        evento_key = pygame.K_DOWN
                    elif linea == "DOWN_UP": # Necesario para soltar agacharse/flotar
                        evento_tipo = pygame.KEYUP
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
                    arduino_serial.close()
                except Exception:
                    pass
                arduino_serial = None 
        # ----------------------------------------------------
        # ⬆️ FIN BLOQUE DE LECTURA SERIAL ⬆️
        # ----------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if arduino_serial and arduino_serial.is_open:
                    arduino_serial.close()
                pygame.quit()
                sys.exit()

            if juego_activo:
                # MODIFICADO: K_UP (D2) ahora es salto
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    # Simulamos un evento de K_SPACE para que "manejar_salto" funcione
                    event_salto = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                    pygame.event.post(event_salto)

                # MODIFICADO: Se restauró la llamada a manejar_agacharse
                jugador.manejar_salto(event)
                jugador.manejar_agacharse(event)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    try:
                        sonido_salto.play()
                    except Exception:
                        pass
                        
            elif event.type == pygame.KEYDOWN:
                # MODIFICADO: K_RIGHT (D3) ahora también reinicia
                if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                    jugador.reiniciar(ALTO, ALTURA_SUELO)
                    obstaculos.empty()
                    aves.empty()
                    puntaje = 0
                    velocidad_juego = 9.0 # ACTUALIZADO: Misma velocidad base
                    juego_activo = True
                    tiempo_ultimo_obstaculo = pygame.time.get_ticks()
                    tiempo_ultima_ave = pygame.time.get_ticks()
                    intervalo_cactus = random.randint(2000, 4000) # ACTUALIZADO: Mismo rango inicial
                    intervalo_ave = random.randint(5000, 9000)
                # MODIFICADO: K_LEFT (D5) ahora también vuelve al menú
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_LEFT:
                    corriendo = False # Termina el bucle de juego
                    # El record se devuelve al final de la función

        if juego_activo:
            # MODIFICADO: Se quitó toda la lógica de DASH
            fondo.actualizar(velocidad_juego)
            jugador.actualizar(dt)
            obstaculos.update()
            aves.update()

            tiempo_actual = pygame.time.get_ticks()

            if tiempo_actual - tiempo_ultima_ave > intervalo_ave:
                aves.add(Ave(ave_imgs, ANCHO, ALTO, velocidad_juego))
                tiempo_ultima_ave = tiempo_actual
                intervalo_ave = random.randint(5000, 9000)

            # --- LÓGICA DE OBSTÁCULOS MODIFICADA ---
            if tiempo_actual - tiempo_ultimo_obstaculo > intervalo_cactus:
                
                # Decidir si generar uno o dos
                if random.random() < CHANCE_DOBLE_CACTUS:
                    # Generar DOS cactus
                    separacion = random.randint(SEPARACION_MIN, SEPARACION_MAX)
                    obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))
                    # El segundo puede ser pequeño
                    obstaculos.add(Obstaculo(cactus_small, ANCHO + cactus_imgs[0].get_width() + separacion, ALTO, ALTURA_SUELO, velocidad_juego))
                else:
                    # Generar UN cactus
                    obstaculos.add(Obstaculo(cactus_imgs, ANCHO, ALTO, ALTURA_SUELO, velocidad_juego))

                # Evitar que un ave aparezca justo después de un cactus
                tiempo_actual_local = pygame.time.get_ticks()
                tiempo_desde_ultima_ave = tiempo_actual_local - tiempo_ultima_ave
                if intervalo_ave - tiempo_desde_ultima_ave < 1000: # Si falta menos de 1s para un ave
                    tiempo_ultima_ave = tiempo_actual_local # Reiniciar timer del ave

                tiempo_ultimo_obstaculo = tiempo_actual
                intervalo_cactus = random.randint(2200, 4500) # AJUSTADO: Rango más alto y consistente
            # --- FIN LÓGICA OBSTÁCULOS ---

            # --- COLISIONES ---
            if pygame.sprite.spritecollide(jugador, obstaculos, False, pygame.sprite.collide_mask) or \
               pygame.sprite.spritecollide(jugador, aves, False, pygame.sprite.collide_mask):
                juego_activo = False
                record = max(record, int(puntaje))
                sonido_gameover.play()

                # === BLOQUE: GUARDAR/ACTUALIZAR PUNTAJE ===
                try:
                    conexion = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="dino"
                    )
                    cursor = conexion.cursor()

                    if id_jugador:
                        puntaje_final = int(puntaje)

                        cursor.execute("SELECT Puntaje FROM ranking WHERE Id_Usuario = %s", (id_jugador,))
                        fila = cursor.fetchone()

                        if fila:
                            puntaje_guardado = fila[0]
                            if puntaje_final > puntaje_guardado:
                                cursor.execute("UPDATE ranking SET Puntaje = %s WHERE Id_Usuario = %s", (puntaje_final, id_jugador))
                                print(f"[DB] Record actualizado: {puntaje_final} pts (Usuario ID {id_jugador})")
                        else:
                            cursor.execute("INSERT INTO ranking (Id_Usuario, Puntaje) VALUES (%s, %s)", (id_jugador, puntaje_final))
                            print(f"[DB] Record guardado: {puntaje_final} pts (Usuario ID {id_jugador})")

                        conexion.commit()
                    else:
                        print("[AVISO] No se guardó el puntaje: jugador sin nombre registrado.")

                    conexion.close()
                except Exception as e:
                    # ⚠️ Este error de DB no afecta la jugabilidad
                    print(f"[ERROR BD] No se pudo guardar el puntaje: {e}")
                # === FIN BLOQUE BD ===

            # --- PUNTAJE ---
            puntaje += 0.1
            if int(puntaje) % 100 == 0 and int(puntaje) > 0 and velocidad_juego < 15:
                velocidad_juego += 0.25

        # --- DIBUJADO ---
        VENTANA.fill(COLOR_ESPACIO_FONDO)
        fondo.dibujar(VENTANA)
        obstaculos.draw(VENTANA)
        aves.draw(VENTANA)
        jugador.dibujar(VENTANA)

        VENTANA.blit(astro_img, astro_img.get_rect(topright=(ANCHO - 20, 20)))

        mostrar_texto(f"Puntos: {int(puntaje)}", 10, 10, BLANCO, VENTANA)
        mostrar_texto(f"Record: {record}", ANCHO - 150, 10, BLANCO, VENTANA)

        if not juego_activo:
            game_over_surf = imagenes_base["game_over"]
            game_over_rect = game_over_surf.get_rect(center=(ANCHO // 2, ALTO // 2 - 50)) # Subir un poco
            VENTANA.blit(game_over_surf, game_over_rect)
            
            # MODIFICADO: Textos actualizados y debajo de la imagen
            mostrar_texto("Presiona DERECHA para reiniciar", ANCHO // 2, game_over_rect.bottom + 40, BLANCO, VENTANA, centrado=True)
            mostrar_texto("Presiona IZQUIERDA para volver al menú", ANCHO // 2, game_over_rect.bottom + 90, BLANCO, VENTANA, centrado=True)

        pygame.display.flip()
    
    # --- Fin del bucle `while corriendo` ---
    return record # Devuelve el record al menú principal

# =================================================================
# ⬆️ FIN NUEVA FUNCIÓN: BUCLE_JUEGO ⬆️
# =================================================================


# --- ESTADO GLOBAL DEL JUEGO ---
personaje_actual = "perro"
mundo_actual = "noche"
record_actual = 0 # El record se actualiza desde bucle_juego

# --- MENÚ PRINCIPAL ---
# MODIFICADO: Se pasa el record_actual y el idioma_actual
menu = Menu(VENTANA, ANCHO, ALTO, record_actual, arduino_serial, idioma_actual) 
menu.nombre_actual = nombre_jugador
menu.id_usuario_actual = id_usuario

# --- BUCLE DE MENÚ PRINCIPAL (REDISEÑADO) ---
while True:
    menu.record_actual = record_actual # Actualiza el record en el menú
    
    opcion_menu = menu.mostrar() # "jugar", "mundo", "personaje", "salir"
    
    # CORREGIDO: El idioma se obtiene del menú DESPUÉS de mostrarlo
    idioma_actual = menu.idioma # <-- ¡MUY IMPORTANTE!

    if opcion_menu == "jugar":
        # Llamar a la función del juego con la configuración actual
        record_actual = bucle_juego(personaje_actual, mundo_actual, nombre_jugador, id_usuario, menu.volumen_sfx, record_actual)
        # Actualizar volumen (por si se cambió en el menú)
        actualizar_volumen_sfx(menu.volumen_sfx)
    
    elif opcion_menu == "mundo":
        # MODIFICADO: Se pasa el idioma
        selector_mundo = SeleccionMundo(VENTANA, ANCHO, ALTO, arduino_serial, idioma_actual) 
        mundo_seleccionado = selector_mundo.mostrar()
        if mundo_seleccionado in ("noche", "dia"):
            mundo_actual = mundo_seleccionado # Actualizar estado global
            
    elif opcion_menu == "personaje":
        # MODIFICADO: Se pasa el idioma
        selector_personaje = SeleccionPersonaje(VENTANA, ANCHO, ALTO, arduino_serial, idioma_actual)
        personaje_seleccionado = selector_personaje.mostrar()
        if personaje_seleccionado in ("perro", "gato"):
            personaje_actual = personaje_seleccionado # Actualizar estado global

    elif opcion_menu == "salir":
        if arduino_serial and arduino_serial.is_open:
            arduino_serial.close()
        pygame.quit()
        sys.exit()

# --- FIN DEL PROGRAMA ---