import pygame
import random

# ==============================
# CLASE PERRO
# ==============================
class Perro(pygame.sprite.Sprite):
    def __init__(self, imagenes_corriendo, imagen_salto, imagen_aire, ancho_ventana, alto_ventana, altura_suelo):
        super().__init__()
        
        self.imagenes_corriendo = imagenes_corriendo
        self.imagen_salto = imagen_salto
        self.imagen_aire = imagen_aire
        self.indice_animacion = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 100
        
        self.image = self.imagenes_corriendo[self.indice_animacion]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.altura_suelo = alto_ventana - altura_suelo
        self.rect.y = self.altura_suelo - self.rect.height
        self.velocidad_y = 0
        self.gravedad = 0.5
        self.en_suelo = True
        self.mask = pygame.mask.from_surface(self.image)
        # Posición fija para el modo boss (opcional: el perro se queda quieto)
        self.posicion_boss_x = 50
    
    def manejar_salto(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.en_suelo:
            self.velocidad_y = -13
            self.en_suelo = False
    
    def actualizar(self, dt, modo_boss=False):
        if not modo_boss:
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y
    
            if self.rect.y >= self.altura_suelo - self.rect.height:
                self.rect.y = self.altura_suelo - self.rect.height
                self.en_suelo = True
                self.velocidad_y = 0
    
                self.tiempo_animacion += dt
                if self.tiempo_animacion >= self.velocidad_animacion:
                    self.indice_animacion = (self.indice_animacion + 1) % len(self.imagenes_corriendo)
                    self.image = self.imagenes_corriendo[self.indice_animacion]
                    self.tiempo_animacion = 0
                    
            else:
                if self.velocidad_y < 0:
                    self.image = self.imagen_salto
                else:
                    self.image = self.imagen_aire
        else:
            # En modo boss, el perro salta/cae pero no corre
            self.velocidad_y += self.gravedad
            self.rect.y += self.velocidad_y

            if self.rect.y >= self.altura_suelo - self.rect.height:
                self.rect.y = self.altura_suelo - self.rect.height
                self.en_suelo = True
                self.velocidad_y = 0
                self.image = self.imagenes_corriendo[0] # Se queda en una pose estática
            
            # Asegurar que la posición x es fija
            self.rect.x = self.posicion_boss_x


        self.mask = pygame.mask.from_surface(self.image)
    
    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
    
    def reiniciar(self, alto_ventana, altura_suelo):
        self.rect.x = 50
        self.rect.y = alto_ventana - altura_suelo - self.rect.height
        self.velocidad_y = 0
        self.en_suelo = True
        self.indice_animacion = 0
        self.tiempo_animacion = 0

# ==============================
# CLASE OBSTACULO (Cactus)
# ==============================
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, imagenes, ancho_ventana, alto_ventana, altura_suelo, velocidad_juego):
        super().__init__()
        self.image = random.choice(imagenes)
        self.rect = self.image.get_rect()
        self.rect.x = ancho_ventana
        self.rect.y = alto_ventana - altura_suelo - self.rect.height
        self.velocidad = velocidad_juego
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.x < -self.rect.width:
            self.kill()

# ==============================
# CLASE FONDO
# ==============================
class Fondo:
    def __init__(self, imagen, velocidad=0.5):
        self.imagen = imagen
        self.velocidad = velocidad
        self.x = 0

    def actualizar(self, velocidad_juego, modo_boss=False):
        if not modo_boss:
            self.x -= self.velocidad * velocidad_juego
            if self.x <= -self.imagen.get_width():
                self.x = 0
        # En modo boss, el fondo puede detenerse o moverse más lento
        # Lo dejaremos quieto por ahora para un efecto de escenario de jefe

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, 0))
        superficie.blit(self.imagen, (self.x + self.imagen.get_width(), 0))

# ==============================
# CLASE PORTAL
# ==============================
class Portal(pygame.sprite.Sprite):
    def __init__(self, imagenes_portal, ancho_ventana, alto_ventana, altura_suelo, velocidad_juego):
        super().__init__()
        self.imagenes = imagenes_portal
        self.indice_animacion = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 150
        
        self.image = self.imagenes[self.indice_animacion]
        self.rect = self.image.get_rect()
        self.rect.x = ancho_ventana
        self.rect.y = alto_ventana - altura_suelo - self.rect.height
        self.velocidad = velocidad_juego
        self.mask = pygame.mask.from_surface(self.image)
        self.activado = False

    def update(self, dt):
        self.rect.x -= self.velocidad
        
        self.tiempo_animacion += dt
        if self.tiempo_animacion >= self.velocidad_animacion:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.imagenes)
            self.image = self.imagenes[self.indice_animacion]
            self.tiempo_animacion = 0
        
        self.mask = pygame.mask.from_surface(self.image)
        
        if self.rect.x < -self.rect.width:
            self.kill()

# ==============================
# CLASE BOSS (JEFE FINAL)
# ==============================
class Boss(pygame.sprite.Sprite):
    def __init__(self, imagenes_boss, ancho_ventana, alto_ventana, altura_suelo):
        super().__init__()
        self.imagenes = imagenes_boss
        self.indice_animacion = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 250 # Lento para pose de ataque
        
        self.image = self.imagenes[self.indice_animacion]
        self.rect = self.image.get_rect()
        # Posicionar al jefe a la derecha, cerca del suelo
        self.rect.x = ancho_ventana - self.rect.width - 50 
        self.rect.y = alto_ventana - altura_suelo - self.rect.height 
        self.mask = pygame.mask.from_surface(self.image)

        # Coordenadas aproximadas de la mano para generar el proyectil (ajustar si es necesario)
        # Se asume que el boss es la misma escala que el perro (150x150) o se ajusta
        self.posicion_generacion_proyectil = (self.rect.x + 20, self.rect.y + self.rect.height / 2 - 20) 
        self.ultima_accion = pygame.time.get_ticks()
        self.intervalo_ataque = 2000 # Ataca cada 2 segundos

    def update(self, dt):
        # Animación del jefe
        self.tiempo_animacion += dt
        if self.tiempo_animacion >= self.velocidad_animacion:
            self.indice_animacion = (self.indice_animacion + 1) % len(self.imagenes)
            self.image = self.imagenes[self.indice_animacion]
            self.tiempo_animacion = 0
        
        self.mask = pygame.mask.from_surface(self.image)

    def debe_atacar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultima_accion > self.intervalo_ataque:
            self.ultima_accion = tiempo_actual
            return True
        return False
    
    def obtener_posicion_bola(self):
        # Devuelve la posición de la mano según el frame de animación (boss1, boss2, boss3)
        # Se requiere ajustar según la imagen. Usaremos una estimación para boss1.
        # boss1.png (pos 0) tiene las manos juntas, bola1.png va allí.
        
        offset_x = 0
        offset_y = 0
        if self.indice_animacion == 0: # boss1.png
            offset_x = 10
            offset_y = 50
        elif self.indice_animacion == 1: # boss2.png
            offset_x = 0
            offset_y = 50
        elif self.indice_animacion == 2: # boss3.png
            offset_x = -30
            offset_y = 50
            
        return (self.rect.x + self.rect.width // 2 + offset_x, self.rect.y + offset_y)
    
    def get_current_bola_img_index(self):
        # Mapea el índice de animación del jefe al índice de la bola de fuego
        return self.indice_animacion 


# ==============================
# CLASE BOLA DE FUEGO (Proyectil del jefe)
# ==============================
class BolaFuego(pygame.sprite.Sprite):
    def __init__(self, imagenes_bola, indice_animacion_boss, pos_inicio, velocidad_juego):
        super().__init__()
        self.imagenes = imagenes_bola
        self.indice_animacion_actual = indice_animacion_boss # Usar el índice del jefe para el inicio
        
        # Elige la imagen inicial según el frame del jefe
        self.image = self.imagenes[self.indice_animacion_actual]
        self.rect = self.image.get_rect()
        self.rect.center = pos_inicio # Comienza en la mano del jefe
        
        self.velocidad = velocidad_juego * 1.5 # Más rápido que el fondo
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.velocidad # Mover de derecha a izquierda
        
        # Animación de la bola: cicla las 4 bolas
        # Usaremos las 4 imágenes de bola de fuego para una animación de vuelo
        self.indice_animacion_actual = (self.indice_animacion_actual + 1) % len(self.imagenes)
        self.image = self.imagenes[self.indice_animacion_actual]
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.x < -self.rect.width:
            self.kill() # Eliminar si sale de la pantalla