import pygame
from lib.gameObject import gameObject
from lib.textObject import textObject

#Класс персонажа
class Person(gameObject):
    def __init__(self, login, x, y, type, rotate='up'):
        gameObject.__init__(self, x, y)
        self.login = login
        self.type = type
        self.spavnx = x
        self.spavny = y
        self.x = x
        self.y = y
        self.coins = 100
        self.cooldown = 10
        self.score = 0
        self.rotate = rotate
        self.items = []

        if type == 'маг':
            self.hp = 100
        elif type == 'воин':
            self.hp = 500
        else:
            self.hp = 200

    def set_coor(self, x, y):
        self.x = x
        self.y = y

    def spavn(self):
        self.x = self.spavnx
        self.y = self.spavny
        if self.type == 'маг':
            self.hp = 100
        elif self.type == 'воин':
            self.hp = 500
        else:
            self.hp = 200

    def move(self, x, y):
        self.x += x
        self.y += y

    def update(self, screen, font):
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.type == 'маг':
            if self.rotate == 'down':
                sprite = pygame.image.load('access/img/magi/player_magi_down.png')
            elif self.rotate == 'up':
                sprite = pygame.image.load('access/img/magi/player_magi_up.png')
            elif self.rotate == 'left':
                sprite = pygame.image.load('access/img/magi/player_magi_left.png')
            elif self.rotate == 'right':
                sprite = pygame.image.load('access/img/magi/player_magi_right.png')

        elif self.type == 'воин':
            if self.rotate == 'down':
                sprite = pygame.image.load('access/img/warrior/player_warrior_down.png')
            elif self.rotate == 'up':
                sprite = pygame.image.load('access/img/warrior/player_warrior_up.png')
            elif self.rotate == 'left':
                sprite = pygame.image.load('access/img/warrior/player_warrior_left.png')
            elif self.rotate == 'right':
                sprite = pygame.image.load('access/img/warrior/player_warrior_right.png')

        elif self.type == 'убийца':
            if self.rotate == 'down':
                sprite = pygame.image.load('access/img/killer/player_killer_down.png')
            elif self.rotate == 'up':
                sprite = pygame.image.load('access/img/killer/player_killer_up.png')
            elif self.rotate == 'left':
                sprite = pygame.image.load('access/img/killer/player_killer_left.png')
            elif self.rotate == 'right':
                sprite = pygame.image.load('access/img/killer/player_killer_right.png')

        else:
            pass

        text_player = font.render(self.login, True, (0, 0, 0))
        text_hp = font.render(str(self.hp) + "hp", True, (0, 0, 0))
        text_type = font.render(self.type, True, (0, 0, 0))

        place_sprite = sprite.get_rect(center=[self.x+25, self.y+25])
        place_text_player =  text_player.get_rect(center=[self.x+25, self.y-7])
        place_text_hp =  text_hp.get_rect(center=[self.x+25, self.y-27])
        place_text_type = text_type.get_rect(center=[self.x+25, self.y-47])

        object_text_player = textObject(self.login, font, screen, place_text_player)
        object_text_hp = textObject(str(self.hp) + "hp", font, screen, place_text_hp)
        object_text_type = textObject(self.type, font, screen, place_text_type)

        object_text_player.update()
        object_text_hp.update()
        object_text_type.update()

        screen.blit(sprite, place_sprite)