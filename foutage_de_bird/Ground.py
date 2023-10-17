import pygame
from sys import exit
import random
from Pipe import scroll_speed, win_height, win_width

ground_image = pygame.image.load("assets/ground.png")
skyline_image = pygame.image.load("assets/background.png")


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()