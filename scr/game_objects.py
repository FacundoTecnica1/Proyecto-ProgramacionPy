import pygame
import random

# ==============================
# CLASE PERRO
# ==============================
# Dentro del archivo game_objects.py

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
    
    def manejar_salto(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.en_suelo:
            self.velocidad_y = -13
            self.en_suelo = False
    
    def actualizar(self, dt):
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
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
    
    def reiniciar(self, alto_ventana, altura_suelo):
        self.rect.y = alto_ventana - altura_suelo - self.rect.height
        self.velocidad_y = 0
        self.en_suelo = True
        self.indice_animacion = 0
        self.tiempo_animacion = 0

# ==============================
# CLASE OBSTACULO
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

    def actualizar(self, velocidad_juego):
        self.x -= self.velocidad * velocidad_juego
        if self.x <= -self.imagen.get_width():
            self.x = 0

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x, 0))
        superficie.blit(self.imagen, (self.x + self.imagen.get_width(), 0))