import pygame
import random

# --- CLASE PERRO / GATO (jugador) ---
class Perro(pygame.sprite.Sprite):
    def __init__(self, frames_correr, imagen_salto, imagen_aire, ancho, alto, altura_suelo):
        super().__init__()
        self.frames_correr = frames_correr
        self.imagen_salto = imagen_salto
        self.imagen_aire = imagen_aire
        self.image = frames_correr[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = alto - altura_suelo
        self.rect.left = 50

        self.altura_suelo = altura_suelo
        self.alto_pantalla = alto
        self.vel_y = 0
        self.gravedad = 1.0
        self.en_suelo = True
        self.frame_index = 0
        self.tiempo_anim = 0

    def manejar_salto(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.en_suelo:
            self.vel_y = -20
            self.en_suelo = False

    def actualizar(self, dt):
        self.vel_y += self.gravedad
        self.rect.y += self.vel_y

        if self.rect.bottom >= self.alto_pantalla - self.altura_suelo:
            self.rect.bottom = self.alto_pantalla - self.altura_suelo
            self.vel_y = 0
            self.en_suelo = True

        # --- Animación ---
        if self.en_suelo:
            self.tiempo_anim += dt
            if self.tiempo_anim > 100:
                self.frame_index = (self.frame_index + 1) % len(self.frames_correr)
                self.image = self.frames_correr[self.frame_index]
                self.tiempo_anim = 0
        else:
            self.image = self.imagen_aire if self.vel_y > 0 else self.imagen_salto

        self.mask = pygame.mask.from_surface(self.image)

    def reiniciar(self, alto, altura_suelo):
        self.rect.bottom = alto - altura_suelo
        self.vel_y = 0
        self.en_suelo = True

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)


# --- CLASE OBSTÁCULO (cactus) ---
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, imagenes, ancho, alto, altura_suelo, velocidad):
        super().__init__()
        self.image = random.choice(imagenes)
        self.rect = self.image.get_rect()
        self.rect.bottom = alto - altura_suelo
        self.rect.left = ancho + random.randint(0, 100)
        self.velocidad = velocidad
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()


# --- CLASE AVE ---
class Ave(pygame.sprite.Sprite):
    def __init__(self, imagenes, ancho, alto, velocidad):
        super().__init__()
        self.imagenes = imagenes
        self.image = imagenes[0]
        self.rect = self.image.get_rect()
        self.rect.left = ancho + 50
        self.rect.y = random.choice([alto - 180, alto - 250])
        self.velocidad = velocidad + 2
        self.frame_index = 0
        self.tiempo_anim = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.velocidad
        self.tiempo_anim += 1
        if self.tiempo_anim > 10:
            self.frame_index = (self.frame_index + 1) % len(self.imagenes)
            self.image = self.imagenes[self.frame_index]
            self.tiempo_anim = 0
        if self.rect.right < 0:
            self.kill()


# --- CLASE FONDO (scroll) ---
class Fondo:
    def __init__(self, imagen, velocidad):
        self.imagen = imagen
        self.velocidad = velocidad
        self.x1 = 0
        self.x2 = imagen.get_width()

    def actualizar(self, velocidad_juego):
        self.x1 -= velocidad_juego * self.velocidad
        self.x2 -= velocidad_juego * self.velocidad

        if self.x1 + self.imagen.get_width() < 0:
            self.x1 = self.x2 + self.imagen.get_width()
        if self.x2 + self.imagen.get_width() < 0:
            self.x2 = self.x1 + self.imagen.get_width()

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x1, 0))
        pantalla.blit(self.imagen, (self.x2, 0))
