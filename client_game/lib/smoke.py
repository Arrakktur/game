import pygame
from lib.item import item

class smoke(item):
    def __init__(self, x, y):
        item.__init__(self, x, y)
        self.health = 1000
        self.price = 10

    def update(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 20, 30))
        self.health -= 1
        if self.health <= 0:
            self.kill = True