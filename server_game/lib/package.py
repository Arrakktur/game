delimiter = '\0'

def get_package(data):
    command = ""
    login = ""
    password = ""
    message = ""
    type = ""
    x = ""
    y = ""
    rotation = ""
    hp = ""
    score = ""
    flag = 0

    for i in data:
        if i != delimiter:
            if flag == 0:
                command += str(i)
            elif flag == 1:
                login += i
            elif flag == 2:
                password += i
            elif flag == 3:
                message += i
            elif flag == 4:
                type += i
            elif flag == 5:
                x += i
            elif flag == 6:
                y += i
            elif flag == 7:
                rotation += i
            elif flag == 8:
                hp += i
            elif flag == 9:
                score += i
        else:
            flag += 1

    map = {'command': command, 'login': login, 'password': password, 'message': message, 'type': type, 'x': x, 'y': y, 'rotation': rotation, 'hp': hp, 'score': score}
    return map

def set_package(command="", login="", password="", message="", type="", x=0, y=0, rotation="", hp=0, score=0):

    data = ""

    # Команда
    data += command + delimiter

    # Логин
    data += login + delimiter

    # Пароль
    data += password + delimiter

    # Сообщение
    data += message + delimiter

    # Класс
    data += type + delimiter

    # Х
    data += str(x) + delimiter

    # У
    data += str(y) + delimiter

    # Поворот
    data += rotation + delimiter

    # ХП
    data += str(hp) + delimiter

    # Очки
    data += str(score) + delimiter

    return data