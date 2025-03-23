import pygame
import sys
import random

pygame.init()

# Setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

bg_img = pygame.transform.scale(pygame.image.load("sprites/background.png").convert(), (WIDTH, HEIGHT))
base_img = pygame.transform.scale(pygame.image.load("sprites/base.png").convert_alpha(), (WIDTH, 100))
pipe_img = pygame.image.load("sprites/pipe.png").convert_alpha()

pipe_gap = 150
pipe_width = pipe_img.get_width()
pipe_height = pipe_img.get_height()
pipe_speed = 3

pipes = []


def create_pipe():
    y_pos = random.randint(200, 400)
    top = pygame.transform.flip(pipe_img, False, True)
    bottom = pipe_img
    return {"top": top, "bottom": bottom, "x": WIDTH, "y": y_pos}

pipes.append(create_pipe())

clock = pygame.time.Clock()
base_x = 0

bird_imgs = [
    pygame.image.load("sprites/upflap.png").convert_alpha(),
    pygame.image.load("sprites/midflap.png").convert_alpha(),
    pygame.image.load("sprites/downflap.png").convert_alpha()
]

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.gravity = 0
        self.flap_index = 0
        self.flap_timer = 0
        self.image = bird_imgs[0]

    def update(self):
        
        self.gravity += 0.5
        self.y += self.gravity

        
        self.flap_timer += 1
        if self.flap_timer >= 5:
            self.flap_timer = 0
            self.flap_index = (self.flap_index + 1) % len(bird_imgs)
            self.image = bird_imgs[self.flap_index]

    def jump(self):
        self.gravity = -8 

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

bird = Bird()
running = True
while running:
    clock.tick(60)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_img, (0, 0))

    for pipe in pipes:
        pipe['x'] -= pipe_speed

        screen.blit(pipe['top'], (pipe['x'], pipe['y'] - pipe_gap - pipe_height))
        screen.blit(pipe['bottom'], (pipe['x'], pipe['y']))

    if pipes[-1]['x'] < WIDTH - 200:
        pipes.append(create_pipe())

    if pipes[0]['x'] < -pipe_width:
        pipes.pop(0)

    base_x -= pipe_speed
    if base_x <= -WIDTH:
        base_x = 0
    screen.blit(base_img, (base_x, HEIGHT - 100))
    screen.blit(base_img, (base_x + WIDTH, HEIGHT - 100))

    bird.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird.jump()

    bird.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
