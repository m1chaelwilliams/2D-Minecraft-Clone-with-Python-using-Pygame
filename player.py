import pygame
from globals import *
from block import Block

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, blocks, inventory, position, image, ID="player", type="none"):
        super().__init__(groups)
        self.groups = groups
        self.ID = ID
        self.type = type

        self.blocks = blocks
        self.inventory = inventory

        self.image = image
        self.rect = self.image.get_rect(topleft = position)

        # physics stuff
        self.velocity = pygame.math.Vector2()

        # mouse stuff
        self.player_offset = pygame.math.Vector2()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x += -1
        if keys[pygame.K_d]:
            self.velocity.x += 1

        # if not left or right
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.velocity.x < 0:
                self.velocity.x += 0.1
            if self.velocity.x > 0:
                self.velocity.x -= 0.1


        # jumping
        if keys[pygame.K_SPACE]:
            self.velocity.y = -PLAYERSPEED * 4

    def move(self):

        self.velocity.y += GRAVITY

        if self.velocity.x > 2:
            self.velocity.x = 2

        if self.velocity.x < -2:
            self.velocity.x = -2
        
        if abs(self.velocity.x) < 0.2:
            self.velocity.x = 0


        if self.velocity.y > 20:
            self.velocity.y = 20
        
        self.rect.x += self.velocity.x * PLAYERSPEED
        self.collision_check("horizontal")
        self.rect.y += self.velocity.y
        self.collision_check("vertical")

    def collision_check(self, direction):
        if direction == "horizontal":
            for block in self.blocks:
                if block.type == "solid":
                    if block.rect.colliderect(self.rect):
                        if self.velocity.x > 0:
                            self.rect.right = block.rect.left
                        if self.velocity.x < 0:
                            self.rect.left = block.rect.right
        if direction == "vertical":
            for block in self.blocks:
                if block.type == "solid":
                    if block.rect.colliderect(self.rect):
                        if self.velocity.y > 0:
                            self.velocity.y = 0.1
                            self.rect.bottom = block.rect.top
                        if self.velocity.y < 0:
                            self.rect.top = block.rect.bottom

    def block_handling(self):
        mouse = pygame.mouse.get_pressed()

        collided_block = False
        for block in self.blocks:
            if block.rect.collidepoint(self.get_adj_mouse_pos()):
                collided_block = True
                block.hovered = True
                if mouse[0]:
                    block.life += 1
                    block.breaking = True
                else:
                    block.life = 0
                    block.breaking = False
                if block.life > block.lifespan:
                    print('breaking block')
                    self.inventory.add_block(block.ID)
                    block.breaking = False
                    block.kill()

            else:
                block.hovered = False

        if not collided_block and mouse[2]:
            self.place_block()
    def place_block(self):
        block = self.inventory.get_active_block()
        if block.ID != "empty" and not self.player_block_bounds().collidepoint(self.get_mouse_block_pos()):
            print('placing')
            Block([self.groups, self.blocks], self.get_mouse_block_pos(), pygame.transform.scale(block.texture, (TILESIZE, TILESIZE)), ID=block.ID, type="solid")
            self.inventory.remove_block()
    def get_mouse_block_pos(self):
        return (int((self.get_adj_mouse_pos()[0]//TILESIZE)*TILESIZE),  int((self.get_adj_mouse_pos()[1]//TILESIZE)*TILESIZE))
    def player_block_bounds(self):
        return pygame.Rect(int((self.rect.x//TILESIZE)*TILESIZE), int((self.rect.y//TILESIZE)*TILESIZE), TILESIZE*2, TILESIZE*2.5)
    def get_adj_mouse_pos(self):
        self.player_offset.x = SCREENWIDTH/2 - self.rect.centerx
        self.player_offset.y = SCREENHEIGHT/2 - self.rect.centery

        return (pygame.mouse.get_pos()[0] - self.player_offset.x, pygame.mouse.get_pos()[1] - self.player_offset.y)
    def update(self):
        self.input()
        self.move()
        self.block_handling()