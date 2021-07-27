#Шифр Вижинера
#Словарь символов для шифрования
def form_dist():
    d = {}
    iter = 0
    for i in range(0, 127):
        d[iter] = chr(i)
        iter = iter + 1
    return d

#Сопоставление букв в словаре с индексами
def encode_val(word):
    list_code = []
    lent = len(word)
    d = form_dist()

    for w in range(lent):
        for value in d:
            if word[w] == d[value]:
                list_code.append(value)
    return list_code

def comparator(value, key):
    len_key = len(key)
    dic = {}
    iter = 0
    full = 0

    for i in value:
        dic[full] = [i,key[iter]]
        full = full + 1
        iter = iter +1
        if (iter >= len_key):
            iter = 0
    return dic

#Сопоставляем индексы ключа с индексами слова
def full_encode(value, key):
    dic = comparator(value, key)
    lis = []
    d = form_dist()

    for v in dic:
        go = (dic[v][0]+dic[v][1]) % len(d)
        lis.append(go)
    return lis

#Переводим в символы
def decode_val(list_in):
    list_code = []
    lent = len(list_in)
    d = form_dist()

    for i in range(lent):
        for value in d:
            if list_in[i] == value:
               list_code.append(d[value])
    return list_code

#Переводим в строку
def decode_str(list_in):
    str = ""
    for i in list_in:
        str += i
    return str

def shifre_v(pas, key):
    pas = encode_val(pas)
    key = encode_val(key)
    shifr = full_encode(pas, key)
    shifr = decode_val(shifr)
    shifr = decode_str(shifr)
    return shifr
