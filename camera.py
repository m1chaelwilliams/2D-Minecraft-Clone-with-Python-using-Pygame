from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup

class Camera(pygame.sprite.Group):
    def __init__(self, display):
        super().__init__()
        self.display = display
    def draw(self):
        for block in self.sprites():
            self.display.blit(block.image, block.rect)
    def draw_centered(self, target):
        offset = pygame.math.Vector2()
        offset.x = self.display.get_width()/2 - target.rect.centerx
        offset.y = self.display.get_height()/2 - target.rect.centery

        for block in self.sprites():
            block_offset = pygame.math.Vector2()
            block_offset.x = offset.x + block.rect.x
            block_offset.y = offset.y + block.rect.y
            
            self.display.blit(block.image, block_offset)
            if block.ID != "player" and block.hovered:
                self.display.blit(block.overlay, block_offset)
        p_offset = pygame.math.Vector2()
        p_offset.x = offset.x + target.rect.x
        p_offset.y = offset.y + target.rect.y   
        self.display.blit(target.image, p_offset)