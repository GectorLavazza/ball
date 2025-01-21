import pygame

from sys import exit
from time import time
import random


SW, SH = 1280, 720
CENTER = SW // 2, SH // 2


class Walls:
    def __init__(self, screen):
        self.screen = screen
        self.walls = [
            pygame.Rect(0, 0, 10, SH),
            pygame.Rect(SW - 10, 0, 10, SH),
            pygame.Rect(0, 0, SW, 10),
            pygame.Rect(0, SH - 10, SW, 10)
        ]

    def update(self):
        for w in self.walls:
            pygame.draw.rect(self.screen, 'red', w)


class Ball(pygame.sprite.Sprite):
    def __init__(self, walls, *group):
        super().__init__(*group)
        self.image = pygame.Surface((50, 50))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(100, SW - 100), random.randint(100, SH - 100)
        self.d = pygame.Vector2(1, 1)
        self.speed = 5
        self.velocity = pygame.Vector2(0, 0)
        self.walls = walls

    def update(self, dt):
        self.velocity.x = self.d.x * dt * self.speed
        self.velocity.y = self.d.y * dt * self.speed

        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        self.check_collision()

    def check_collision(self):
        for w in self.walls.walls:
            if self.rect.colliderect(w):
                if self.walls.walls.index(w) in (0, 1):
                    self.d.x *= -1
                else:
                    self.d.y *= -1


def main():
    pygame.init()
    pygame.display.set_caption('Ball')

    flags = pygame.DOUBLEBUF
    screen = pygame.display.set_mode((SW, SH), flags, depth=8, vsync=1)

    clock = pygame.time.Clock()

    ball_g = pygame.sprite.Group()

    walls = Walls(screen)
    ball = Ball(walls, ball_g)

    last_time = time()

    running = 1
    st = time()

    while running:

        dt = time() - last_time
        dt *= 60
        last_time = time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = 0

                if event.key == pygame.K_F10:
                    pygame.display.toggle_fullscreen()

        screen.fill('black')

        walls.update()

        ball_g.update(dt)
        ball_g.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()