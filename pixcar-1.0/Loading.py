import pygame
import utils
import math
import copy

class Loading(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.image, self.rect = utils.load_image("loading3.png")
        self.original = copy.copy(self.image)
        self.angle = 0

    def update(self):
        self.angle -= math.radians(360)
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center
