import pygame
from blockdata import *

class Block(pygame.sprite.Sprite):
    def __init__(self, groups, position, image, ID="block", type="solid"):
        super().__init__(groups)
        self.ID = ID
        self.type = type

        # image / rect stuff
        self.standard_img = image
        self.overlay = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
        self.overlay.fill((255,255,255,128))
        self.image = self.standard_img
        self.rect = self.image.get_rect(topleft = position)

        # breaking stuff
        self.hovered = False
        self.breaking = False
        self.count = 0
        self.lifespan = DEFAULTLIFESPAN
        self.life = 0
    def update(self):
        pass