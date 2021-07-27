import socket
import gui.main_gui as main_gui
import configparser
import lib.package
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from game_class import Game_class

""" Загрузка параметров """
config = configparser.ConfigParser()
config.read("config.ini")

#Главное окно
class MainApp(QtWidgets.QMainWindow, main_gui.Ui_MainWindow):
    def __init__(self, login):
        super().__init__()
        self.setupUi(self)
        self.login = login

        self.label.setText("Ваш логин: " + login)
        self.lineEdit.setText(config["Server"]["host"])
        self.lineEdit_4.setText(config["Server"]["port_client"])

        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.set_config)
        self.pushButton_3.clicked.connect(self.post_message)
        self.pushButton_4.clicked.connect(self.get_message)

        self.textEdit.setReadOnly(True)
        self.comboBox.addItem("маг")
        self.comboBox.addItem("воин")
        self.comboBox.addItem("убийца")

        # Для отправки и получения сообщений
        self.sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sor.bind(('', 0))

        self.get_message()

    def message(self, icon, title, text, button):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(button)
        msg.exec_()

    def connect(self):
        # Формируем запрос
        data = lib.package.set_package(command='c', login=self.login)

        # Отправляем запрос на сервер
        self.sor.sendto(data.encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

        # Получаение ответа от сервера
        data = self.sor.recv(1024).decode('utf-8')

        # Подключение к комнате
        if data == '0':
            self.close()
            type = self.comboBox.currentText()
            game = Game_class(self.login, type)
            game.start()
        else:
            self.message(QMessageBox.Critical, "Ошибка", "Ошибка ", QMessageBox.Cancel)

    def set_config(self):
        host = self.lineEdit.text()
        port_client = self.lineEdit_4.text()
        config.set('Server', 'host', str(host))
        config.set('Server', 'port_client', str(port_client))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("done")

    def post_message(self):
        message = self.lineEdit_5.text()

        # Создаем запрос
        data = lib.package.set_package(command='m', login=self.login, message=message)

        # Отправляем запрос на сервер
        self.sor.sendto(data.encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

        # Обновляем окно
        self.get_message()
        self.lineEdit_5.setText("")

    def get_message(self):

        # Создаем запрос
        data = lib.package.set_package(command='g')

        # делаем запрос к серверу
        self.sor.sendto(data.encode('utf-8'), (config["Server"]["host"], int(config["Server"]["port_client"])))

        # Получаем сообщение от сервера
        data = self.sor.recv(1024).decode('utf-8')

        # Декодируем ответ сервера
        map = lib.package.get_package(data)
        data = map["message"]

        # Переформатирование текста
        message = ""
        login = ""
        text = ""
        flag = 0
        for i in data:
            if i == "/":
                if flag == 0:
                    flag = 1
                    if self.login == login:
                        message += "<font color=\"Red\">" + login + "</font>: "
                    else:
                        message += "<font color=\"Green\">" + login + "</font>: "
                    login = ""
                else:
                    flag = 0
                    message += "<font color=\"Black\">" + text + "</font><br>"
                    text = ""
                continue
            if i == "!":
                break
            if flag == 0:
                login += i
            if flag == 1:
                text += i

        # Отображаем сообщения
        self.textEdit.setHtml(message)