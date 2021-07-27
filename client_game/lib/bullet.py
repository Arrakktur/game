import pygame
import configparser

""" Загрузка параметров """
config = configparser.ConfigParser()
config.read("config.ini")

#Класс персонажа
class Bullet:
    def __init__(self, x, y, speedx, speedy, login):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.login = login
        self.color = (255, 100, 255)
        self.kill = False

    def get_coor(self):
        return self.x, self.y

    def set_coor(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x < 0 or self.y < 0 or self.x > int(config["Game"]["width"]) or self.y > int(config["Game"]["height"]):
            self.kill = True

    def update(self, screen):
        self.move()
        sprite = pygame.image.load('access/img/bullet.png')
        screen.blit(sprite, (self.x, self.y))