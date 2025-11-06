import pygame
import random

# ==============================
# CLASE AVE (Versión principal)
# ==============================
class Ave(pygame.sprite.Sprite):
    def __init__(self, imagenes, ancho_ventana, alto_ventana, velocidad_juego):
        super().__init__()
        
        self.imagenes = imagenes
        self.indice_animacion = 0
        self.image = self.imagenes[self.indice_animacion]
        self.tiempo_animacion = 0
        self.velocidad_animacion = 150  

        # --- Posición y movimiento ---
        self.rect = self.image.get_rect()
        self.rect.x = ancho_ventana
        # MODIFICADO: Rango de altura de vuelo
        self.rect.y = random.choice([alto_ventana - 180, alto_ventana - 250, alto_ventana - 320])
        self.velocidad = velocidad_juego + random.uniform(1.5, 3.0) # Velocidad variable
        # MODIFICADO: Se quitó _base_vel
        self.mask = pygame.mask.from_surface(self.image)
        self.ultimo_update = pygame.time.get_ticks()

    def update(self):
        # Mover el ave hacia la izquierda
        self.rect.x -= self.velocidad
        
        # Animar el ave
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_update > self.velocidad_animacion:
            self.ultimo_update = ahora
            self.indice_animacion = (self.indice_animacion + 1) % len(self.imagenes)
            self.image = self.imagenes[self.indice_animacion]
            # Es importante actualizar la máscara si la imagen cambia
            self.mask = pygame.mask.from_surface(self.image)

        # Eliminar el sprite si sale de la pantalla
        if self.rect.right < 0:
            self.kill()


# ==============================
# CLASE PERRO / GATO (jugador)
# ==============================
class Perro(pygame.sprite.Sprite):
    # --- MODIFICADO: __init__ (Se quitó el Dash) ---
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
        # Agachado
        self.is_crouching = False
        # Tecla abajo presionada
        self.down_pressed = False
        # Tecla espacio presionada
        self.space_pressed = False
        # Agachado en aire (flotar)
        self.air_crouch = False
        
        # Guardar ancho para limitar dash
        self.ancho = ancho
        # Guardar referencias originales para restaurar
        self._original_frames_correr = list(frames_correr)
        self._original_imagen_salto = imagen_salto
        self._original_imagen_aire = imagen_aire
        # Guardar gravedad original para ajustar caída en el aire
        self._original_gravedad = self.gravedad

    # --- MODIFICADO: manejar_salto (Se quitó el Dash) ---
    def manejar_salto(self, event):
        # Manejar presionar/soltar SPACE para salto
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.space_pressed = True
            # comportamiento normal de salto (solo si estamos en suelo)
            if self.en_suelo:
                self.vel_y = -20
                self.en_suelo = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.space_pressed = False

    # --- MODIFICADO: manejar_agacharse (Se quitó el Dash) ---
    def manejar_agacharse(self, event):
        """Maneja eventos KEYDOWN/KEYUP para la tecla de agacharse (flecha abajo)."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            
            # Si estamos en el aire y estamos cayendo, activar flotación
            # MODIFICADO: Se quitó 'and not self.is_dashing'
            if not self.en_suelo and self.vel_y > 0: 
                self.air_crouch = True
                # Reducir gravedad y limitar velocidad para sensación más notable de flotación
                self.gravedad = self._original_gravedad * 0.25
                if self.vel_y > 3:
                    self.vel_y = 3
            elif self.en_suelo:
                self.crouch()
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self.down_pressed = False
            # Si estaba flotando en el aire, restaurar gravedad
            if self.air_crouch:
                self.air_crouch = False
                self.gravedad = self._original_gravedad
            elif self.is_crouching:
                self.stand_up()

    # --- MODIFICADO: Se eliminó _try_start_dash() ---

    # --- MÉTODO crouch() (Restaurado) ---
    def crouch(self):
        """Aplica el efecto de agacharse.

        - En suelo: comprime la altura a la mitad (comportamiento existente).
        - En el aire: activa "air_crouch" que reduce la gravedad para que el jugador
          "flote" y caiga más despacio.
        """
    # Si ya está agachado en suelo, no hacer nada
        if self.en_suelo:
            if self.is_crouching:
                return
            self.is_crouching = True
            # Guardar posición inferior para mantener al suelo
            bottom = self.rect.bottom
            left = self.rect.left

            # Escalar los frames de correr y las imágenes de salto/aire verticalmente a la mitad
            def half_height(img):
                w, h = img.get_size()
                new_h = max(1, h // 2)
                return pygame.transform.smoothscale(img, (w, new_h))

            self.frames_correr = [half_height(img) for img in self._original_frames_correr]
            self.imagen_salto = half_height(self._original_imagen_salto)
            self.imagen_aire = half_height(self._original_imagen_aire)

            # Actualizar la imagen actual según el estado (en suelo: frame de correr)
            self.frame_index = self.frame_index % len(self.frames_correr)
            self.image = self.frames_correr[self.frame_index]

            # Actualizar rect y máscara, manteniendo la posición inferior
            self.rect = self.image.get_rect()
            self.rect.left = left
            self.rect.bottom = bottom
            self.mask = pygame.mask.from_surface(self.image)
        # Nota: el comportamiento de agachado en el aire (flotar) se gestiona
        # desde manejar_agacharse para distinguir entre subir y caer.

    # --- MÉTODO stand_up() (Restaurado) ---
    def stand_up(self):
        """Restaura la altura original del jugador y actualiza rect y máscara."""
        if not self.is_crouching:
            return
        self.is_crouching = False
        bottom = self.rect.bottom
        left = self.rect.left

        # Restaurar imágenes originales
        self.frames_correr = list(self._original_frames_correr)
        self.imagen_salto = self._original_imagen_salto
        self.imagen_aire = self._original_imagen_aire

        # Restaurar imagen actual según estado
        if self.en_suelo:
            self.frame_index = self.frame_index % len(self.frames_correr)
            self.image = self.frames_correr[self.frame_index]
        else:
            self.image = self.imagen_aire if self.vel_y > 0 else self.imagen_salto

        # Actualizar rect y máscara, manteniendo la posición inferior
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)

    # --- MODIFICADO: actualizar (Se quitó el Dash) ---
    def actualizar(self, dt):
        
        # Aplicar gravedad y movimiento vertical normal
        self.vel_y += self.gravedad

        # MODIFICADO: Se eliminó la revisión de 'dash' por frame
        
        self.rect.y += self.vel_y

        # Limita la posición al suelo
        if self.rect.bottom >= self.alto_pantalla - self.altura_suelo:
            self.rect.bottom = self.alto_pantalla - self.altura_suelo
            self.vel_y = 0
            self.en_suelo = True
            # Si aterrizamos y estábamos en modo air_crouch, restaurar gravedad
            if self.air_crouch:
                self.air_crouch = False
                self.gravedad = self._original_gravedad

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

    # --- MODIFICADO: reiniciar (Se quitó el Dash) ---
    def reiniciar(self, alto, altura_suelo):
        # Restaurar posición y estados básicos
        self.rect = self.image.get_rect()
        self.rect.left = 50
        self.rect.bottom = alto - altura_suelo
        self.vel_y = 0
        self.gravedad = self._original_gravedad
        self.en_suelo = True
        # Restaurar estados de entrada/agachado
        self.is_crouching = False
        self.down_pressed = False
        self.air_crouch = False # <-- Añadido para seguridad
        
        # Restaurar imágenes y frames originales
        self.frames_correr = list(self._original_frames_correr)
        self.imagen_salto = self._original_imagen_salto
        self.imagen_aire = self._original_imagen_aire
        self.frame_index = 0
        self.image = self.frames_correr[self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)


# ==============================
# CLASE OBSTÁCULO (Cactus)
# ==============================
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, imagenes, ancho, alto, altura_suelo, velocidad):
        super().__init__()
        self.image = random.choice(imagenes)
        self.rect = self.image.get_rect()
        self.rect.bottom = alto - altura_suelo
        self.rect.left = ancho + random.randint(0, 50) # Menos aleatoriedad
        
        # MODIFICADO: Se quitó _base_vel, ya no es necesario
        self.velocidad = velocidad
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()


# ==============================
# CLASE AVE (Versión usada en main)
# ==============================
# (Se eliminó la definición duplicada, la primera es la que vale)


# ==============================
# CLASE FONDO (scroll)
# ==============================
class Fondo:
    def __init__(self, imagen, velocidad):
        self.imagen = imagen
        self.velocidad = velocidad
        self.x1 = 0
        self.x2 = imagen.get_width()

    def actualizar(self, velocidad_juego):
        # MODIFICADO: Se quitó la multiplicación por dash
        self.x1 -= velocidad_juego * self.velocidad
        self.x2 -= velocidad_juego * self.velocidad

        if self.x1 + self.imagen.get_width() < 0:
            self.x1 = self.x2 + self.imagen.get_width()
        if self.x2 + self.imagen.get_width() < 0:
            self.x2 = self.x1 + self.imagen.get_width()

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x1, 0))
        pantalla.blit(self.imagen, (self.x2, 0))