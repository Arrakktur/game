import socket
import time
import pygame
import sys
import configparser
import lib.package

from lib.ward import ward
from lib.smoke import smoke
from lib.hward import hward
from lib.person import Person
from lib.bullet import Bullet
from lib.textObject import textObject
from threading import Thread

""" Загрузка параметров """
config = configparser.ConfigParser()
config.read("config.ini")

# Удаление элемента из словаря
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

# Окно игры
class Game_class:
    def __init__(self, login, type):
        self.players = [] # Список игроков
        self.bullets = [] # Список выстрелов
        self.textObjects = {} # Список текстовых объектов
        self.items = {} # Список предметов
        self.wards = [] # Список вардов

        # Игрок
        self.player = Person(login, int(int(config["Game"]["width"])/2), int(int(config["Game"]["height"])/2), type, 'down')

        # Для отправки данных серверу
        self.sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sor.bind(('', 0))

    # Для получения данных с сервера
    def read_sok(self):
        while 1:
            data = self.sor.recv(1024).decode('utf-8')
            map = lib.package.get_package(data)
            command = map['command']

            if command == 'p':
                login = map['login']
                x = map['x']
                y = map['y']
                type = map['type']
                rotate = map['rotation']
                hp = map['hp']
                score = map['score']
                flag = 0
                for player in self.players:
                    if player.login == login:
                        flag = 1
                        player.x = int(x)
                        player.y = int(y)
                        player.rotate = rotate
                        player.hp = hp
                        player.score = score
                        break
                if flag == 0:
                    p = Person(login, int(x), int(y), type, rotate)
                    self.players.append(p)

            elif command == 'd':
                login = map['login']
                for player in self.players:
                    if login == player.login:
                        self.players.remove(player)

            elif command == 'b':
                x = map['x']
                y = map['y']
                speedx = map['speedx']
                speedy = map['speedy']
                login = map['login']
                bullet = Bullet(int(x), int(y), int(speedx), int(speedy), login)
                self.bullets.append(bullet)

            elif command == 's':
                login = map['login']
                if self.player.login == login:
                    self.player.score += 1
                    self.player.coins += 1
                else:
                    for i in self.players:
                        if i.login == login:
                            i.score += 1
                            i.coins += 1

            elif command == 'w':
                x = map['x']
                y = map['y']
                item = ward(int(x), int(y))
                item.visible = False
                self.wards.append(item)

    def start(self):
        #Получение сообщений от сервера
        potok = Thread(target=self.read_sok)
        potok.start()

        # События игры
        pygame.font.init()
        font = pygame.font.SysFont('access/fonts/ofont.ttf', 26)
        screen = pygame.display.set_mode((int(config["Game"]["width"]), int(config["Game"]["height"])))

        # Запуск таймера
        clock = pygame.time.Clock()
        start_time = time.time()

        # Загрузка фона
        background_image = pygame.image.load('access/img/bg.jpg')

        # Инициализация GUI
        text_score = textObject(self.player.login + ': ' + str(self.player.score), font, screen, (50, 20))
        text_countPlayers = textObject('Count players: ' + str(len(self.players) + 1), font, screen, (500, 20))
        text_FPS = textObject('FPS: 0', font, screen, (1000, 20))
        text_coins = textObject('Coins: ' + str(self.player.coins), font, screen, (50, int(config['Game']['height'])-50))
        text_items = textObject('Items:   HWard 5   Smoke 10   Ward 5', font, screen, (850, int(config['Game']['height'])-50))

        self.textObjects['text_score'] = text_score
        self.textObjects['text_countPlayers'] = text_countPlayers
        self.textObjects['text_FPS'] = text_FPS
        self.textObjects['text_coins'] = text_coins
        self.textObjects['text_items'] = text_items

        while 1:
            # Обрабатываем события
            for i in pygame.event.get():

                # Событие выхода из игры
                if i.type == pygame.QUIT:

                    # Формируем запрос
                    data = lib.package.set_package(command='d', login=self.player.login)

                    # Отправляем на сервер
                    self.sor.sendto((data).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

                    # Формируем запрос
                    data = lib.package.set_package(command='e', login=self.player.login)

                    # Отправляем на сервер
                    self.sor.sendto((data).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

                    # Закрываем игру
                    pygame.quit()
                    sys.exit()

            #Загружаем фон
            screen.blit(background_image, (0, 0))

            # Игрок
            self.player.update(screen, font)

            # Проверка получения урона
            for bul in self.bullets:
                if (bul.x > self.player.x and bul.x < self.player.x+25 and bul.y > self.player.y and bul.y < self.player.y+50 and bul.login != self.player.login):
                    self.player.hp -= 1
                    if self.player.hp < 0:
                        self.player.spavn()
                        message = lib.package.set_package(command='s', login=bul.login)
                        self.sor.sendto((message).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

            # Враги
            for i in self.players:
                i.update(screen, font)

            # Выстрелы
            for i in self.bullets:
                i.update(screen)
                if i.kill == True:
                    self.bullets.remove(i)

            # Предметы
            for i in self.items:
                self.items[i].update(screen)
                if self.items[i].kill == True:
                    self.items = removekey(self.items, i)

            # HWard
            if 'hward' in self.items:
                dist = ((self.player.x - self.items['hward'].x)**2 + (self.player.y - self.items['hward'].y)**2)**(1/2)
                if dist <= self.items['hward'].dist:
                    self.player.hp += 1

            # Ward
            for i in self.wards:
                i.update(screen)
                if i.kill == True:
                    self.wards.remove(i)
                else:
                    dist = ((self.player.x - i.x) ** 2 + (self.player.y - i.y) ** 2) ** (1 / 2)
                    if dist <= i.dist and self.player.hp > 1:
                        self.player.hp -= 1

            # Изменение GUI
            self.textObjects['text_FPS'].text =  'FPS: ' + str(round(1.0 / (time.time() - start_time)))
            self.textObjects['text_countPlayers'].text = 'Count players: ' + str(len(self.players) + 1)
            self.textObjects['text_score'].text = self.player.login + ': ' + str(self.player.score)
            self.textObjects['text_coins'].text = "Coins: " + str(self.player.coins)

            # Счетчик времени для FPS
            start_time = time.time()

            # Отрисовка GUI
            for text in self.textObjects:
                self.textObjects[text].update()

            y = 40
            for i in self.players:
                text = textObject(i.login + ": " + str(i.score), font, screen, (50, y))
                text.update()
                y += 20

            # Обновление экрана
            pygame.display.update()

            # Действия игрока
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.player.x >= 0:
                    self.player.move(-3, 0)
                    self.player.rotate = 'left'
            if keys[pygame.K_RIGHT]:
                if self.player.x <= int(config["Game"]["width"]) - 50:
                    self.player.move(3, 0)
                    self.player.rotate = 'right'
            if keys[pygame.K_UP]:
                if self.player.y >= 50:
                    self.player.move(0, -3)
                    self.player.rotate = 'up'
            if keys[pygame.K_DOWN]:
                if self.player.y <= int(config["Game"]["height"]) - 50:
                    self.player.move(0, 3)
                    self.player.rotate = 'down'
            if keys[pygame.K_SPACE]:
                if self.player.cooldown == 0:
                    self.player.cooldown = 10
                    if self.player.rotate == 'up':
                        speedx = 0
                        speedy = -10
                    elif self.player.rotate == 'down':
                        speedx = 0
                        speedy = 10
                    elif self.player.rotate == 'right':
                        speedx = 10
                        speedy = 0
                    elif self.player.rotate == 'left':
                        speedx = -10
                        speedy = 0

                    bullet = Bullet(self.player.x, self.player.y, speedx, speedy, self.player.login)
                    self.bullets.append(bullet)

                    # Формируем запрос
                    data = lib.package.set_package(command='b', x=self.player.x, y=self.player.y, speedx=speedx, speedy=speedy, login=self.player.login)

                    # Отправка на сервер
                    self.sor.sendto((data).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

            # Вард
            if keys[pygame.K_q]:
                item = hward(self.player.x, self.player.y)
                if self.player.coins >= item.price and 'hward' not in self.items:
                    self.items['hward'] = item
                    self.player.coins -= item.price

            if keys[pygame.K_w]:
                item = smoke(self.player.x, self.player.y)
                if self.player.coins >= item.price and 'smoke' not in self.items:
                    self.items['smoke'] = item
                    self.player.coins -= item.price

            if keys[pygame.K_e]:
                item = ward(self.player.x, self.player.y)
                if self.player.coins >= item.price and 'ward' not in self.items:
                    self.items['ward'] = item
                    self.player.coins -= item.price

                    # Формируем запрос
                    data = lib.package.set_package(command='w', x=self.player.x, y=self.player.y, login=self.player.login)

                    # Отправка на сервер
                    self.sor.sendto((data).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

            # Отправляем сообщение на сервер
            data = lib.package.set_package(command='p', login=self.player.login, x=self.player.x, y=self.player.y, type=self.player.type, rotation=self.player.rotate, hp=self.player.hp, score=self.player.score)
            self.sor.sendto((data).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

            clock.tick(int(config["Game"]["fps"]))