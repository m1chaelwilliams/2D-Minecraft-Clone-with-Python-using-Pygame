import pygame
import sys

from world import World
from events import EventHandler
from globals import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

        self.world = World(self.screen)

    def draw(self):
        self.screen.fill('lightblue')

        self.world.draw()
        
    def update(self):
        self.world.update()
        
    def run(self):
        while True:
            EventHandler.run()
            for event in EventHandler.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw()
            self.update()
            

            self.clock.tick(60)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()