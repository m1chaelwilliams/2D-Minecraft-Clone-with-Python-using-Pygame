import pygame
from player import Player
from block import Block
from globals import *
from camera import Camera
from inventory import Inventory
import random
import noise

class World:
    def __init__(self, display):
        self.display = display

        # sprite groups
        self.visible_sprites = Camera(display)
        self.blocks = pygame.sprite.Group()

        

        self.textures = self.gen_textures()
        self.gen_world()

        # inventory stuff
        self.inventory = Inventory(self.display, self.textures)

        self.player = Player([self.visible_sprites], self.blocks, self.inventory, (50,50), pygame.Surface((TILESIZE*0.8,TILESIZE*1.5)))

    def gen_textures(self) -> dict:
        atlas = pygame.image.load('res/atlas.png').convert()

        textures = {}

        textures['grass'] = pygame.transform.scale(atlas.subsurface(pygame.Rect(ATLASTILESIZE*3, 0, ATLASTILESIZE, ATLASTILESIZE)), (TILESIZE, TILESIZE))
        textures['dirt'] = pygame.transform.scale(atlas.subsurface(pygame.Rect(ATLASTILESIZE*2, 0, ATLASTILESIZE, ATLASTILESIZE)), (TILESIZE, TILESIZE))
        textures['planks'] = pygame.transform.scale(atlas.subsurface(pygame.Rect(ATLASTILESIZE*4, 0, ATLASTILESIZE, ATLASTILESIZE)), (TILESIZE, TILESIZE))
        textures['stone'] = pygame.transform.scale(atlas.subsurface(pygame.Rect(ATLASTILESIZE*1, 0, ATLASTILESIZE, ATLASTILESIZE)), (TILESIZE, TILESIZE))
        textures['wood'] = pygame.transform.scale(atlas.subsurface(pygame.Rect(ATLASTILESIZE*4, ATLASTILESIZE, ATLASTILESIZE, ATLASTILESIZE)), (TILESIZE, TILESIZE))
        textures['leaves'] = pygame.transform.scale(pygame.image.load('res/pack2.png').convert_alpha(), (TILESIZE, TILESIZE))

        return textures
    def gen_world(self):


        # Display the terrain
        prevoff = 0
        for x in range(-50, 50):
            offset = prevoff + random.randint(-1, 1)
            for y in range(20-offset):
                blocktype = "dirt"
                if y < 20-offset - 3:
                    blocktype = "stone"
                if y == 20-offset-1:
                    if random.randint(0,15) == 1:
                        self.spawn_tree(x,y)
                    blocktype = "grass"
                Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - y*TILESIZE), self.textures[blocktype], ID=blocktype)
    def spawn_tree(self, x, y):
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+1)*TILESIZE), self.textures["wood"], type="wall", ID="wood")
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+2)*TILESIZE), self.textures["wood"], type="wall", ID="wood")
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+3)*TILESIZE), self.textures["wood"], type="wall", ID="wood")
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+4)*TILESIZE), self.textures["wood"], type="wall", ID="wood")
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+5)*TILESIZE), self.textures["wood"], type="wall", ID="wood")

        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+4)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+5)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], (x*TILESIZE, 20*TILESIZE - (y+6)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x-1)*TILESIZE, 20*TILESIZE - (y+4)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x-1)*TILESIZE, 20*TILESIZE - (y+5)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x-1)*TILESIZE, 20*TILESIZE - (y+6)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x-2)*TILESIZE, 20*TILESIZE - (y+4)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x-2)*TILESIZE, 20*TILESIZE - (y+5)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x+1)*TILESIZE, 20*TILESIZE - (y+4)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x+1)*TILESIZE, 20*TILESIZE - (y+5)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x+1)*TILESIZE, 20*TILESIZE - (y+6)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x+2)*TILESIZE, 20*TILESIZE - (y+4)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")
        Block([self.visible_sprites, self.blocks], ((x+2)*TILESIZE, 20*TILESIZE - (y+5)*TILESIZE), self.textures["leaves"], type="wall", ID="leaves")



    def draw(self):
        self.visible_sprites.draw_centered(self.player)
        self.inventory.draw()
    def update(self):
        self.visible_sprites.update()
        self.inventory.update()
