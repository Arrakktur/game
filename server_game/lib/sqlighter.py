import sqlite3

class SQLighter:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_aut(self, login, password):
        sql = "SELECT count(id), autorize FROM users WHERE login='" + login + "' AND password='" + password + "'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = data[0]
        return data

    def set_aut(self, login, data):
        sql = "UPDATE users SET autorize=" + str(data) + " WHERE login='" + login + "'"
        self.cursor.execute(sql)
        self.connection.commit()

    def reg(self, login, password):
        sql = "INSERT INTO users (login, password, autorize) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (login, password, 0))
        self.connection.commit()

    def new_message(self, login, message):
        sql = "INSERT INTO message (user, text) VALUES (?, ?)"
        self.cursor.execute(sql, (login, message))
        self.connection.commit()

    def get_message(self):
        sql = "SELECT user, text FROM message ORDER BY id DESC LIMIT 30"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def close(self):
        """ Закрываем соединение с базой данных """
        self.connection.close()