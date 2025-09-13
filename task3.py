import pygame, random, math

WIDTH, HEIGHT = 800, 600
NUM_DRONES = 150
MAX_SPEED = 3
NEIGHBOR_DIST = 50
SEPARATION_FORCE = 0.08
MOUSE_FORCE = 0.15

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swarm Remix")
clock = pygame.time.Clock()

class Drone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.color = (random.randint(100,255), random.randint(50,200), random.randint(100,255))

    def update(self, swarm, mouse_pos):
        steer = pygame.math.Vector2(0, 0)
        for other in swarm:
            if other == self: continue
            dist = self.pos.distance_to(other.pos)
            if 0 < dist < NEIGHBOR_DIST:
                diff = self.pos - other.pos
                steer += diff / dist
        if mouse_pos:
            diff = self.pos - pygame.math.Vector2(mouse_pos)
            dist = diff.length()
            if dist < 100 and dist > 0:
                steer += diff / dist * MOUSE_FORCE

        self.vel += steer * SEPARATION_FORCE
        if self.vel.length() > MAX_SPEED:
            self.vel = self.vel.normalize() * MAX_SPEED
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        angle = self.vel.angle_to(pygame.math.Vector2(1, 0))
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, self.color, [(0, 8), (16, 4), (16, 12)])
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=self.pos)

drones = pygame.sprite.Group()
for _ in range(NUM_DRONES):
    drones.add(Drone(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

running = True
while running:
    mouse_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()

    for d in drones:
        d.update(drones, mouse_pos)

    screen.fill((15, 15, 30))
    drones.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
