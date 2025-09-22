import pygame
import random

# Inicialización Pygame
pygame.init()

# Pantalla
WIDTH, HEIGHT = 500, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaurio con Pygame")

# Cargar imágenes
DINO_IMG = pygame.image.load("dino_custom.png").convert_alpha()      # Imagen del dinosaurio con la cabeza
CACTUS1 = pygame.image.load("cactus1.png").convert_alpha()          # Primer cactus
CACTUS2 = pygame.image.load("cactus2.png").convert_alpha()          # Segundo cactus
BACKGROUND = pygame.image.load("background.png").convert_alpha()    # Fondo (paisaje lunar)
GAME_OVER_IMG = pygame.image.load("game_over.png").convert_alpha()  # Game Over

# Variables y constantes
GROUND_LEVEL = HEIGHT - 70
GRAVITY = 1
JUMP_VEL = -15
CACTUS_SPEED = 7

FONT = pygame.font.SysFont('Arial', 24)

class Dinosaur:
    def __init__(self):
        self.image = DINO_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_LEVEL - self.rect.height
        self.vel_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_VEL
            self.is_jumping = True

    def move(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.is_jumping = False

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Cactus:
    def __init__(self):
        self.image = random.choice([CACTUS1, CACTUS2])
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 200)
        self.rect.y = GROUND_LEVEL - self.rect.height

    def move(self):
        self.rect.x -= CACTUS_SPEED

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

def main():
    run = True
    clock = pygame.time.Clock()
    dinosaur = Dinosaur()
    cactuses = [Cactus()]
    score = 0
    game_over = False

    while run:
        clock.tick(30)
        WIN.fill((255, 255, 255))
        WIN.blit(BACKGROUND, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dinosaur.jump()
                if event.key == pygame.K_r and game_over:
                    # Reiniciar juego
                    dinosaur = Dinosaur()
                    cactuses = [Cactus()]
                    score = 0
                    game_over = False

        if not game_over:
            dinosaur.move()
            dinosaur.draw(WIN)

            # Mover y dibujar cactus
            rem = []
            add_cactus = False
            for cactus in cactuses:
                cactus.move()
                cactus.draw(WIN)
                if cactus.rect.right < 0:
                    rem.append(cactus)
                if not add_cactus and cactus.rect.centerx < WIDTH // 2:
                    add_cactus = True

                # Colisión
                if dinosaur.rect.colliderect(cactus.rect):
                    game_over = True

            if add_cactus:
                cactuses.append(Cactus())
            for r in rem:
                cactuses.remove(r)

            # Puntaje
            score += 1
            score_text = FONT.render(f"Puntaje: {score//10}", True, (0, 0, 0))
            WIN.blit(score_text, (600, 20))
        else:
            # Mostrar texto Game Over
            WIN.blit(GAME_OVER_IMG, ((WIDTH - GAME_OVER_IMG.get_width()) // 2,
                                     (HEIGHT - GAME_OVER_IMG.get_height()) // 2))

            reiniciar_text = FONT.render("Presiona R para reiniciar", True, (255, 255, 255))
            WIN.blit(reiniciar_text, ((WIDTH - reiniciar_text.get_width()) // 2,
                                      (HEIGHT - GAME_OVER_IMG.get_height()) // 2 + 70))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
