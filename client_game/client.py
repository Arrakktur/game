import socket
import gui.autorize as autorize
import sys
import configparser
import lib.package
from lib.shifr_viginer import shifre_v
from main_class import MainApp
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets

""" Загрузка параметров """
config = configparser.ConfigParser()
config.read("config.ini")

login = ""

#Окно авторизации
class AutorizeApp(QtWidgets.QMainWindow, autorize.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.autorize)
        self.pushButton_2.clicked.connect(self.registration)

        # Для отправки данных серверу
        self.sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sor.bind(('', 0))

    def message(self, icon, title, text, button):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(button)
        msg.exec_()

    def request(self, command):
        global login
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Валидация
        if login == "" or password == "":
            self.message(QMessageBox.Critical, "Ошибка", "Нужно ввести логин и пароль", QMessageBox.Cancel)
            return

        # Шифруем пароль
        shifre = shifre_v(password, config["Game"]["key"])

        # Кодируем запрос
        data = lib.package.set_package(command=command, login=login, password=shifre)

        #Отправляем запрос на сервер
        self.sor.sendto((data).encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

        #Получаем ответ от сервера
        data = self.sor.recv(1024)
        data = data.decode('utf-8')
        return data

    def registration(self):
        data = self.request('r')
        if data == '':
            self.message(QMessageBox.Critical, "Ошибка", "Ошибка сервера", QMessageBox.Cancel)
        elif data == "0":
            self.message(QMessageBox.Information, "Успешно", "Регистрация прошла успешно", QMessageBox.Ok)
        elif data == "1":
            self.message(QMessageBox.Critical, "Ошибка", "Логин уже занят", QMessageBox.Cancel)
        else:
            self.message(QMessageBox.Critical, "Ошибка", "Ошибка регистрации", QMessageBox.Cancel)

    def autorize(self):
        data = self.request('a')
        if data == '':
            self.message(QMessageBox.Critical, "Ошибка", "Ошибка сервера", QMessageBox.Cancel)
        elif data == "0":
            self.window = MainApp(login)
            self.window.show()
            self.close()
        elif data == "1":
            self.message(QMessageBox.Critical, "Ошибка", "Неверный логин или пароль", QMessageBox.Cancel)
        elif data == "2":
            self.message(QMessageBox.Critical, "Ошибка", "Пользователь уже авторизован", QMessageBox.Cancel)
        else:
            self.message(QMessageBox.Critical, "Ошибка", "Ошибка авторизации", QMessageBox.Cancel)

def main():
    #Запускаем окно авторизации
    app = QtWidgets.QApplication(sys.argv)
    window = AutorizeApp()
    window.show()
    app.exec_()

    # Выход из игры
    sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sor.bind(('', 0))

    # Создаем запрос
    data = lib.package.set_package(command='e', login=login)

    # Отправляем запрос на сервер
    sor.sendto(data.encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

if __name__ == '__main__':
    main()
