import pygame
from lib.item import item

class ward(item):
    def __init__(self, x, y):
        item.__init__(self, x, y)
        self.health = 1000
        self.price = 5

    def update(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (225, 0, 0), (self.x, self.y, 20, 30))
        self.health -= 1
        if self.health <= 0:
            self.kill = True