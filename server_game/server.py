import socket
import configparser
import lib.package
from lib.sqlighter import SQLighter

""" Загрузка параметров """
config = configparser.ConfigParser()
config.read("config.ini")

""" Массив с подключенными клиентами """
client = []

# Главные сокет для обработки запросов
def client_socket():
    # Подключение к базе данных
    database = SQLighter(config["Database"]["db_name"])

    # Создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((config["Server"]["HOST"], int(config["Server"]["socket_client"])))

    # Список клиентов
    global client

    # Запускаем прослушивание сокета
    while True:
        data, address = sock.recvfrom(1024)
        data = data.decode('utf-8')

        # Парсим запрос
        map = lib.package.get_package(data)
        command = map['command']

        # Авторизация
        if command == 'a':

            login = map['login']
            password = map['password']

            # Делаем запрос к базе данных
            count, data = database.get_aut(login, password)

            # Авторизация удачна
            if count == 1 and data == 0:
                database.set_aut(login, 1)
                sock.sendto(b'0', address)
                print("Autorize " + login + "(" + str(address) + ")")

            #Неверный логин или пароль
            elif count == 0:
                sock.sendto(b'1', address)
                print("Failed autorize: " + login + "(" + str(address) + ") error login or password")

            # Пользователь уже авторизован
            elif data == 1:
                sock.sendto(b'2', address)
                print("Failed autorize: " + login + "(" + str(address) + ") user alredy autorize")

        # Регистрация
        elif command == 'r':

            login = map['login']
            password = map['password']

            #Делаем запрос к базе данных
            count = database.get_aut(login, password)[0]

            #Удачная регистрация
            if count == 0:
                database.reg(login, password)
                sock.sendto(b'0', address)
                print("Registration: " + login + "(" + str(address) + ")")

            #Пользователь уже зерегестрирован
            elif count != 0:
                sock.sendto(b'1', address)
                print("Failed registration: " + login + "(" + str(address) + ") user alredy registration")

        # Подключение к комнате
        elif command == 'c':

            login = map['login']

            sock.sendto(b'0', address)
            print(login + "(" + str(address) + ") connect to server")

        # Выход из игры
        elif command == 'e':

            login = map['login']

            database.set_aut(login, 0)
            print(login + "(" + str(address) + ") disconnect to server")

        # Получение сообщения
        elif command == 'm':

            login = map['login']
            message = map['message']

            database.new_message(login, message)
            print("new message " + login + "(" + str(address) + ") " + message)

        # Отправка сообщений
        elif command == 'g':
            data = database.get_message()
            message = ""
            for i in data:
                message += i[0]
                message += "/"
                message += i[1]
                message += "/"

            data = lib.package.set_package(message=message)
            sock.sendto(bytes(data, encoding='utf-8'), address)

        # Запросы без участия сервера
        else:
            if address not in client:
                client.append(address) # Если такого клиента нет, то добавляем в массив
            for clients in client:
                if clients == address:
                    continue
                sock.sendto(data.encode('utf-8'), clients)

if __name__ == "__main__":
    print("Starting server...")
    client_socket()