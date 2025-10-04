import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Learning how to create game")

# Colors
WHITE = (255,255,255)
BLUE = (50,100,200)
RED = (200,50,50)

# Clock
clock = pygame.time.Clock()
#Player
class Player:
    def __init__(self):
        self.image = pygame.image.load("drone.png")  # load image
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))  # resize
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - PLAYER_SIZE))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED

    def draw(self):
        screen.blit(self.image, self.rect) 

# Enemy 
class Enemy:
    def __init__(self):
        self.size = 40
        self.x = random.randint(0, WIDTH - self.size)
        self.y = 0
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:  
            self.rect.y = -self.size
            self.rect.x = random.randint(0, WIDTH - self.size)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# Creating objects
player = Player()
enemy = Enemy()

# Game loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.move()
    enemy.move()

    # Collision 
    if player.rect.colliderect(enemy.rect):
        print("Collision! Game Over")
        running = False
    player.draw(screen)
    enemy.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
