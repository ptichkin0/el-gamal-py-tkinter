import tkinter as tk
from tkinter import W, E, END
from functools import partial
import random
from math import pow

a = random.randint(2, 10)

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b;
    else:
        return gcd(b, a % b)


# Генерация больших случайных чисел
def generate_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)  # Генерируем пока нод не станет = 1

    return key


# Возведение в степень по модулю
def exp(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c



def encrypt(msg, q, h, g):
    """Шифрование"""
    encrypt_msg = []
    key = generate_key(q)  # ключ отправителя
    s = exp(h, key, q)  # общий секрет
    p = exp(g, key, q)  # C1(В интерфейсе перепутаны обозначения с С2)

    for i in range(0, len(msg)):
        encrypt_msg.append(msg[i])  # дублируем массив

    for i in range(0, len(encrypt_msg)):
        encrypt_msg[i] = s * ord(encrypt_msg[i])  # получаем C2

    return encrypt_msg, p  # Боб отправляет зашифрованный текст (С1,С2) Алисе.


def decrypt(encrypt_msg, p, key, q):
    """Алиса расшифровывает зашифрованный текст (С1,С2) с помощью своего закрытого ключа"""

    decrypt_msg = []
    h = exp(p, key, q)
    for i in range(0, len(encrypt_msg)):
        decrypt_msg.append(chr(int(encrypt_msg[i] / h)))

    return decrypt_msg


"""Генерация ключей и запуск шифрования"""
def encF(text_resultMsg, n1):

    msg = (n1.get())
    q = random.randint(pow(10, 20), pow(10, 50))  # случайное простое число
    g = random.randint(2, q)  # Выбирается случайное целое число
    key = generate_key(q)  # генерация закрытого
    h = exp(g, key, q)  # возведение в степень по модулю
    encrypt_msg, p = encrypt(msg, q, h, g)  # (q,h,g) - открытый ключ, key - закрытый

    resultMsg = f"\n Закодированное сообщение: " \
                f"\n С1: {encrypt_msg}" \
                f"\n С2: {p}" \
                f"\n Ключ: {key}" \
                f"\n q: {q}"

    text_resultMsg.insert(1.0, resultMsg)
    return



"""Расшифрование"""
def decF(text_resultMsg, c1, c2, k, n4):
    msg = c1.get()
    arrMsg = msg.split(", ")
    str_to_int = list(map(int, arrMsg))
    p = (int(c2.get()))
    key = (int(k.get()))
    q = (int(n4.get()))
    dr_msg = decrypt(str_to_int, p, key, q)
    decrypt_msg = ''.join(dr_msg)
    resultMsg = f"\n Раскодированное сообщение: {decrypt_msg}"
    text_resultMsg.insert(1.0, resultMsg)
    return

def clean(text_resultMsg):
    text_resultMsg.delete(1.0, END)

root = tk.Tk()
root.geometry('650x590')

root.title('El Gamal')

number1 = tk.StringVar()
number2 = tk.StringVar()
number3 = tk.StringVar()
number4 = tk.StringVar()

labelSender = tk.Label(root, text="Отправитель").grid(row=0, sticky=W)
labelNum1 = tk.Label(root, text="Введите сообщение(C1):").grid(row=1, column=0, sticky=E)
textResultMsg = tk.Text(root)
tk.Label(root, text="Решение").grid(row=10, column=0, sticky=W)
textResultMsg.grid(row=11, columnspan=3, sticky=W+E)


entryEn = tk.Entry(root, textvariable=number1).grid(row=1, column=1, columnspan=3, sticky=W+E)



encF = partial(encF, textResultMsg, number1)
decF = partial(decF, textResultMsg, number1, number2, number3, number4)
clean = partial(clean, textResultMsg)
buttonEn = tk.Button(root, text="Зашифровать", command=encF).grid(row=2, column=0)

tk.Label(root, text="Получатель").grid(row=5, sticky=W)
tk.Label(root, text="C2:").grid(row=6, column=0, sticky=E)
tk.Label(root, text="Key:").grid(row=7, column=0, sticky=E)
tk.Label(root, text="q:").grid(row=8, column=0, sticky=E)
entryC2 = tk.Entry(root, textvariable=number2).grid(row=6, column=1, columnspan=3, sticky=W+E)
entryKey = tk.Entry(root, textvariable=number3).grid(row=7, column=1, columnspan=3, sticky=W+E)
entryQ = tk.Entry(root, textvariable=number4).grid(row=8, column=1, columnspan=3, sticky=W+E)
buttonD = tk.Button(root, text="Расшифровать", command=decF).grid(row=9)
buttonClr = tk.Button(root, text="Отчистить", command=clean).grid(row=10, column=2, sticky=E)
root.mainloop()
