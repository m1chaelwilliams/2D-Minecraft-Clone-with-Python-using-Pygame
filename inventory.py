import pygame
from globals import *
from events import EventHandler

class Inventory:
    def __init__(self, display, textures) -> None:
        self.display = display
        self.textures = textures
        Inventory.slot_count = 9
        Inventory.spacing = SLOTSIZE/2
        Inventory.halfspacing = SLOTSIZE/4
        
        Inventory.offset = (SCREENWIDTH-(SLOTSIZE*Inventory.slot_count + Inventory.spacing*(Inventory.slot_count-1)))/2
        Inventory.container = pygame.Rect(Inventory.offset-Inventory.halfspacing, SCREENHEIGHT-75-Inventory.halfspacing, (SLOTSIZE*Inventory.slot_count + Inventory.spacing*(Inventory.slot_count-1))+SLOTSIZE/2, SLOTSIZE*1.5)
    
        self.active_slot = 0

        self.first_slot = 0

        self.slots = []
        for slot in range(Inventory.slot_count):
            self.slots.append(Slot(self.display, self.textures, (Inventory.offset + slot*SLOTSIZE + (slot*Inventory.spacing), SCREENHEIGHT-75)))
        
        # inventory expanded

        self.expanded_inventory = False
        self.bound_slot = None
        self.bound_slot_pos = None

        self.expanded_slots = []
        for slot in range(3):
            self.expanded_slots.append(Slot(self.display, self.textures, (Inventory.offset + slot*SLOTSIZE + (slot*Inventory.spacing)-2*TILESIZE, SCREENHEIGHT-TILESIZE*3)))
        for slot in range(3):
            self.expanded_slots.append(Slot(self.display, self.textures, (Inventory.offset + slot*SLOTSIZE + (slot*Inventory.spacing)-2*TILESIZE, SCREENHEIGHT-TILESIZE*2)))

        

        # crafting

        self.crafting = [
            ["empty", "empty"],
            ["empty", "empty"]
        ]

        self.crafting_slots = []
        for slot in range(2):
            self.crafting_slots.append(Slot(self.display, self.textures, (Inventory.offset + slot*SLOTSIZE - TILESIZE + (slot*Inventory.spacing), SCREENHEIGHT-TILESIZE*6)))
        for slot in range(2):
            self.crafting_slots.append(Slot(self.display, self.textures, (Inventory.offset + slot*SLOTSIZE - TILESIZE + (slot*Inventory.spacing), SCREENHEIGHT-TILESIZE*5)))

        self.crafting_output_slot = Slot(self.display, self.textures, (Inventory.offset + slot*SLOTSIZE + (slot*Inventory.spacing), SCREENHEIGHT-TILESIZE*5.5))

        self.slots.extend(self.expanded_slots)


        self.click_delay = -1
    
    def draw(self):
        
        pygame.draw.rect(self.display, "darkgray", Inventory.container)
        self.slots[self.active_slot].highlight()

        for slot in range(Inventory.slot_count):
            self.slots[slot].draw_frame()


        if self.expanded_inventory:
            pygame.draw.rect(self.display, "darkgray", pygame.Rect(TILESIZE, TILESIZE, SCREENWIDTH-TILESIZE*9, SCREENHEIGHT-TILESIZE*2))

            # draw inventory slots
            for slot in self.expanded_slots:
                slot.draw_frame()
            for slot in self.expanded_slots:
                slot.draw()
            # draw crafting slots
            for slot in self.crafting_slots:
                slot.draw_frame()
            for slot in self.crafting_slots:
                slot.draw()    
            self.crafting_output_slot.draw_frame()
            self.crafting_output_slot.draw()


        for slot in range(Inventory.slot_count):
            self.slots[slot].draw()
    def update(self):

        for event in EventHandler.events:
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0:
                    if self.active_slot < self.slot_count-1:
                        self.active_slot += 1
                    else:
                        self.active_slot = 0
                if event.y > 0:
                    if self.active_slot > 0:
                        self.active_slot -= 1
                    else:
                        self.active_slot = 8
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.expanded_inventory = not self.expanded_inventory
        if self.expanded_inventory:
            self.click_delay -= 1

            mouse = pygame.mouse.get_pressed()
            for slot in self.slots:
                if slot.ID != "empty" and mouse[0] and self.bound_slot == None and slot.rect.collidepoint(pygame.mouse.get_pos())  and self.click_delay < 0:

                    
                    self.click_delay = 20

                    self.bound_slot = slot
                    self.bound_slot_pos = slot.rect.center
            for slot in self.crafting_slots:
                if slot.ID != "empty" and mouse[0] and self.bound_slot == None and slot.rect.collidepoint(pygame.mouse.get_pos())  and self.click_delay < 0:

                    
                    self.click_delay = 20

                    self.bound_slot = slot
                    self.bound_slot_pos = slot.rect.center
            if self.crafting_output_slot.ID != "empty" and mouse[0] and self.bound_slot == None and self.crafting_output_slot.rect.collidepoint(pygame.mouse.get_pos())  and self.click_delay < 0:
                    print('picking up')
                    self.click_delay = 20

                    self.bound_slot = self.crafting_output_slot
                    self.bound_slot_pos = self.crafting_output_slot.rect.center

                    for slot in self.crafting_slots:
                        slot.ID = "empty"
                        slot.amount = 0
            
            if self.bound_slot != None:
                
                self.bound_slot.rect.center = pygame.mouse.get_pos()

                if mouse[0] and self.click_delay < 0:
                    

                    self.click_delay = 20

                    seated = False
                    for slot in self.slots:
                        if slot.ID == "empty" and slot.rect.collidepoint(pygame.mouse.get_pos()):
                            if slot != self.bound_slot:
                                slot.ID = self.bound_slot.ID
                                slot.amount = self.bound_slot.amount
                                slot.update_texture()
                                self.bound_slot.rect.center = self.bound_slot_pos
                                self.bound_slot.amount = 0
                                self.bound_slot.ID = "empty"
                                seated = True
                    if not seated:
                        for slot in self.crafting_slots:
                            if slot.ID == "empty" and slot.rect.collidepoint(pygame.mouse.get_pos()):
                                if slot != self.bound_slot:
                                    slot.ID = self.bound_slot.ID
                                    slot.amount = self.bound_slot.amount
                                    slot.update_texture()
                                    self.bound_slot.rect.center = self.bound_slot_pos
                                    self.bound_slot.amount = 0
                                    self.bound_slot.ID = "empty"
                                    seated = True
                                    self.crafting_output_slot.ID = self.check_crafting()
                                    self.crafting_output_slot.update_texture()
                                    self.crafting_output_slot.amount += 1
                    if not seated:
                        self.bound_slot.rect.center = self.bound_slot_pos
                        self.bound_slot = None
                        self.bound_slot_pos = None    
                        print('not seated')


                    self.bound_slot = None
                    self.bound_slot_pos = None
    
    def check_crafting(self) -> str:
        self.crafting = [
            [self.crafting_slots[0], self.crafting_slots[1]],
            [self.crafting_slots[2], self.crafting_slots[3]],
        ]

        # temp
        return "planks"

    def add_block(self, ID, amt=1):
        nearest_slot = 0
        near_slot_bool = False
        for i, slot in enumerate(self.slots):
            if slot.ID == ID:
                print(slot.ID)
                slot.amount += amt
                slot.update_texture()
                print(self.slots[0].ID,self.slots[1].ID,self.slots[2].ID,self.slots[3].ID,self.slots[4].ID,self.slots[5].ID,self.slots[6].ID,self.slots[7].ID,self.slots[8].ID)
                return
            elif slot.ID == "empty" and not near_slot_bool:
                near_slot_bool = True
                nearest_slot = i
                print(self.slots[0].ID,self.slots[1].ID,self.slots[2].ID,self.slots[3].ID,self.slots[4].ID,self.slots[5].ID,self.slots[6].ID,self.slots[7].ID,self.slots[8].ID)

                
        self.slots[nearest_slot].ID = ID
        self.slots[nearest_slot].amount += amt
        self.slots[nearest_slot].update_texture()
        
    def remove_block(self):
        self.slots[self.active_slot].amount -= 1
        if self.slots[self.active_slot].amount <= 0:
            self.slots[self.active_slot].ID = "empty"
            print(self.slots[0].ID,self.slots[1].ID,self.slots[2].ID,self.slots[3].ID,self.slots[4].ID,self.slots[5].ID,self.slots[6].ID,self.slots[7].ID,self.slots[8].ID)

    def get_active_block(self):
        return self.slots[self.active_slot]

class Slot:
    def __init__(self, display, textures, pos, ID="empty") -> None:
        self.display = display
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], SLOTSIZE, SLOTSIZE)
        self.amount = 0
        self.ID = "empty"
        if self.ID != "empty":
            self.texture = pygame.transform.scale(textures[self.ID], (SLOTSIZE, SLOTSIZE))
        self.textures = textures

        self.font = pygame.font.Font(None, 30)
    def update_texture(self):
        self.texture = pygame.transform.scale(self.textures[self.ID], (SLOTSIZE, SLOTSIZE))
    def highlight(self):
        pygame.draw.rect(self.display, "white", pygame.Rect(self.pos[0]-(SLOTSIZE/4), self.pos[1]-(SLOTSIZE/4), SLOTSIZE*1.5, SLOTSIZE*1.5))
    def draw_frame(self):
        pygame.draw.rect(self.display, "gray", pygame.Rect(self.pos[0], self.pos[1], SLOTSIZE, SLOTSIZE))
    def draw(self):
        
        if self.ID != "empty":
            self.display.blit(self.texture, self.rect)
            self.text = self.font.render(str(self.amount), True, "white", None)
            self.display.blit(self.text, self.rect)


        


    