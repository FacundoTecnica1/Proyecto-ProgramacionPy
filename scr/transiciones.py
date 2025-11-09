import pygame
import math
import random

class TransicionPantalla:
    """Clase para manejar transiciones entre pantallas/submenús"""
    
    def __init__(self, ventana, ancho, alto):
        self.ventana = ventana
        self.ancho = ancho
        self.alto = alto
        
    def transicion_deslizar_horizontal(self, superficie_saliente, superficie_entrante, direccion="derecha", duracion=500):
        """
        Transición de deslizamiento horizontal
        direccion: 'derecha', 'izquierda'
        """
        clock = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while True:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio
            
            if tiempo_transcurrido >= duracion:
                break
                
            # Progreso de 0 a 1
            progreso = tiempo_transcurrido / duracion
            progreso_suave = self._ease_in_out_cubic(progreso)
            
            # Calcular posiciones
            if direccion == "derecha":
                pos_saliente = -self.ancho * progreso_suave
                pos_entrante = self.ancho * (1 - progreso_suave)
            else:  # izquierda
                pos_saliente = self.ancho * progreso_suave
                pos_entrante = -self.ancho * (1 - progreso_suave)
            
            # Dibujar
            self.ventana.fill((0, 0, 0))  # Fondo negro
            self.ventana.blit(superficie_saliente, (pos_saliente, 0))
            self.ventana.blit(superficie_entrante, (pos_entrante, 0))
            
            pygame.display.flip()
            clock.tick(60)
    
    def transicion_fade(self, superficie_saliente, superficie_entrante, duracion=300):
        """Transición de desvanecimiento (fade)"""
        clock = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while True:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio
            
            if tiempo_transcurrido >= duracion:
                break
                
            # Progreso de 0 a 1
            progreso = tiempo_transcurrido / duracion
            progreso_suave = self._ease_in_out_quad(progreso)
            
            # Calcular alphas
            alpha_saliente = int(255 * (1 - progreso_suave))
            alpha_entrante = int(255 * progreso_suave)
            
            # Dibujar
            self.ventana.fill((0, 0, 0))
            
            # Superficie saliente con alpha
            superficie_temp = superficie_saliente.copy()
            superficie_temp.set_alpha(alpha_saliente)
            self.ventana.blit(superficie_temp, (0, 0))
            
            # Superficie entrante con alpha
            superficie_temp = superficie_entrante.copy()
            superficie_temp.set_alpha(alpha_entrante)
            self.ventana.blit(superficie_temp, (0, 0))
            
            pygame.display.flip()
            clock.tick(60)
    
    def transicion_zoom_spiral(self, superficie_saliente, superficie_entrante, duracion=600):
        """Transición en espiral con zoom - LA MEJOR SEGÚN EL USER"""
        clock = pygame.time.Clock()
        tiempo_inicio = pygame.time.get_ticks()
        
        while True:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio
            
            if tiempo_transcurrido >= duracion:
                break
                
            # Progreso de 0 a 1
            progreso = tiempo_transcurrido / duracion
            progreso_suave = self._ease_in_out_cubic(progreso)
            
            # Efectos de zoom y rotación MÁS ÉPICOS
            escala_saliente = 1 + progreso_suave * 0.8  # Se agranda más
            rotacion_saliente = progreso_suave * 720  # DOS vueltas completas
            
            escala_entrante = 0.2 + progreso_suave * 0.8  # Aparece desde más pequeño
            alpha_entrante = int(255 * progreso_suave)
            
            # Dibujar fondo espacial épico
            self.ventana.fill((5, 5, 20))
            
            # Añadir estrellas que se mueven
            for i in range(30):
                estrella_x = (50 + i * 25 + tiempo_transcurrido * 0.1) % self.ancho
                estrella_y = (50 + (i * 17) % self.alto + tiempo_transcurrido * 0.05) % self.alto
                brillo = int(128 + 127 * math.sin(tiempo_transcurrido * 0.01 + i))
                pygame.draw.circle(self.ventana, (brillo, brillo, 255), 
                                 (int(estrella_x), int(estrella_y)), 2)
            
            # Superficie saliente (girando y haciéndose grande) CON EFECTOS
            superficie_rotada = pygame.transform.rotozoom(superficie_saliente, rotacion_saliente, escala_saliente)
            rect_rotada = superficie_rotada.get_rect(center=(self.ancho//2, self.alto//2))
            
            alpha_saliente = int(255 * (1 - progreso_suave))
            superficie_rotada.set_alpha(alpha_saliente)
            
            # Solo dibujar si está visible
            if alpha_saliente > 0:
                self.ventana.blit(superficie_rotada, rect_rotada)
            
            # EFECTO DE ONDAS EXPANSIVAS
            centro_x, centro_y = self.ancho // 2, self.alto // 2
            for j in range(3):
                radio_onda = int(300 * progreso_suave - j * 50)
                if radio_onda > 0 and radio_onda < 400:
                    alpha_onda = max(0, 100 - j * 30)
                    color_onda = (100 + j * 50, 200 - j * 40, 255)
                    pygame.draw.circle(self.ventana, color_onda, (centro_x, centro_y), radio_onda, 3)
            
            # Superficie entrante (apareciendo con zoom)
            superficie_zoom = pygame.transform.scale(superficie_entrante, 
                                                   (int(self.ancho * escala_entrante), 
                                                    int(self.alto * escala_entrante)))
            rect_zoom = superficie_zoom.get_rect(center=(self.ancho//2, self.alto//2))
            superficie_zoom.set_alpha(alpha_entrante)
            self.ventana.blit(superficie_zoom, rect_zoom)
            
            # Partículas durante la transición MÁS ÉPICAS
            self._dibujar_particulas_epicas(progreso, tiempo_transcurrido)
            
            pygame.display.flip()
            clock.tick(60)
    
    def _dibujar_particulas_epicas(self, progreso, tiempo_transcurrido):
        """Dibuja partículas SÚPER ÉPICAS durante las transiciones"""
        centro_x, centro_y = self.ancho // 2, self.alto // 2
        
        # Partículas principales (más grandes y brillantes)
        for i in range(12):
            angulo = (progreso * 1080 + i * 30) % 360  # TRES vueltas completas
            radio = 60 + progreso * 250
            
            x = centro_x + radio * math.cos(math.radians(angulo))
            y = centro_y + radio * math.sin(math.radians(angulo))
            
            if 0 <= x <= self.ancho and 0 <= y <= self.alto:
                # Colores que cambian con el tiempo
                r = int(255 * abs(math.sin(tiempo_transcurrido * 0.01 + i)))
                g = int(255 * abs(math.cos(tiempo_transcurrido * 0.008 + i)))
                b = 255
                color = (r, g, b)
                pygame.draw.circle(self.ventana, color, (int(x), int(y)), 5)
                
                # Estela de la partícula
                for j in range(3):
                    radio_estela = radio - j * 10
                    x_estela = centro_x + radio_estela * math.cos(math.radians(angulo))
                    y_estela = centro_y + radio_estela * math.sin(math.radians(angulo))
                    alpha_estela = 100 - j * 30
                    color_estela = (r//2, g//2, b//2)
                    pygame.draw.circle(self.ventana, color_estela, (int(x_estela), int(y_estela)), 3)
        
        # Partículas secundarias (más pequeñas, en dirección contraria)
        for i in range(20):
            angulo = (-progreso * 720 + i * 18) % 360  # Dirección contraria
            radio = 30 + progreso * 150
            
            x = centro_x + radio * math.cos(math.radians(angulo))
            y = centro_y + radio * math.sin(math.radians(angulo))
            
            if 0 <= x <= self.ancho and 0 <= y <= self.alto:
                color = (255, 255 - int(progreso * 100), 100 + int(progreso * 155))
                pygame.draw.circle(self.ventana, color, (int(x), int(y)), 2)
    
    def _dibujar_particulas_transicion(self, progreso):
        """Dibuja partículas durante las transiciones"""
        centro_x, centro_y = self.ancho // 2, self.alto // 2
        
        for i in range(15):
            angulo = (progreso * 720 + i * 24) % 360  # Dos vueltas completas
            radio = 50 + progreso * 200
            
            x = centro_x + radio * math.cos(math.radians(angulo))
            y = centro_y + radio * math.sin(math.radians(angulo))
            
            if 0 <= x <= self.ancho and 0 <= y <= self.alto:
                color = (255, 255 - int(progreso * 100), 100 + int(progreso * 155))
                pygame.draw.circle(self.ventana, color, (int(x), int(y)), 3)
    
    def _ease_in_out_cubic(self, t):
        """Función de suavizado cúbica"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def _ease_in_out_quad(self, t):
        """Función de suavizado cuadrática"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2

def capturar_pantalla(ventana):
    """Captura la pantalla actual como superficie"""
    return ventana.copy()

def transicion_entre_pantallas(ventana, ancho, alto, funcion_pantalla_actual, funcion_pantalla_nueva, tipo_transicion="deslizar_derecha"):
    """
    Función helper para hacer transiciones automáticamente
    """
    transicion = TransicionPantalla(ventana, ancho, alto)
    
    # Capturar pantalla actual
    superficie_saliente = capturar_pantalla(ventana)
    
    # Renderizar nueva pantalla (sin mostrarla)
    superficie_entrante = pygame.Surface((ancho, alto))
    funcion_pantalla_nueva(superficie_entrante)  # La función debe dibujar en la superficie
    
    # Ejecutar transición
    if tipo_transicion == "deslizar_derecha":
        transicion.transicion_deslizar_horizontal(superficie_saliente, superficie_entrante, "derecha")
    elif tipo_transicion == "deslizar_izquierda":
        transicion.transicion_deslizar_horizontal(superficie_saliente, superficie_entrante, "izquierda")
    elif tipo_transicion == "fade":
        transicion.transicion_fade(superficie_saliente, superficie_entrante)
    elif tipo_transicion == "zoom_spiral":
        transicion.transicion_zoom_spiral(superficie_saliente, superficie_entrante)