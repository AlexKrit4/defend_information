# -*- coding: utf-8 -*-
"""
Лабораторная работа № 6. Вариант 11.
Парольная защита методом ВЫБОРКИ СИМВОЛОВ.

Пользователь никогда не вводит пароль целиком: при каждой попытке
входа система по датчику случайных чисел выбирает несколько позиций
пароля и просит ввести только символы на этих позициях. Набор позиций
меняется от попытки к попытке, поэтому перехват введённых символов
не раскрывает пароль полностью.

Дополнительно: ограничение числа попыток (3), отсутствие эха при вводе
(символы маскируются '*'), вывод времени последнего удачного входа.
"""

import os
import sys
import random
import datetime

PASS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "passwd.dat")
MAX_ATTEMPTS = 3          # число попыток до блокировки


def read_char():
    """Ввод одного символа без эха (эхо заменяется на '*')."""
    if not sys.stdin.isatty():            # ввод перенаправлен - читаем stdin
        while True:
            ch = sys.stdin.read(1)
            if ch == "":
                raise EOFError("ввод завершён")
            if ch not in ("\r", "\n"):
                break
        print("*")
        return ch
    try:
        import msvcrt                      # Windows
        ch = msvcrt.getwch()
        if ch in ("\r", "\n"):
            print()
            return read_char()
        if ch == "\x03":
            raise KeyboardInterrupt
        print("*", end="", flush=True)
        return ch
    except ImportError:
        return sys.stdin.read(1)


def setup_password():
    """Первая регистрация: создание файла пароля."""
    while True:
        p1 = input("Задайте пароль (не менее 6 символов): ").strip()
        if len(p1) >= 6:
            break
        print("Слишком короткий пароль!")
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        f.write(p1 + "\n-\n")               # пароль + метка времени входа
    print("Пароль сохранён.\n")


def load_password():
    """Чтение пароля и времени последнего входа."""
    with open(PASS_FILE, encoding="utf-8") as f:
        lines = f.read().splitlines()
    return lines[0], (lines[1] if len(lines) > 1 else "-")


def save_timestamp(ts):
    password, _ = load_password()
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        f.write(password + "\n" + ts + "\n")


def sample_positions(length, count):
    """Случайная выборка count различных позиций пароля (1..length)."""
    return sorted(random.sample(range(length), min(count, length)))


def authenticate():
    password, last = load_password()
    print(f"Время последнего удачного входа: {last}")

    n_ask = max(2, len(password) // 2)     # спрашиваем ~половину позиций
    for attempt in range(1, MAX_ATTEMPTS + 1):
        positions = sample_positions(len(password), n_ask)
        print(f"\nПопытка {attempt} из {MAX_ATTEMPTS}.")
        print("Введите символы пароля на позициях:",
              ", ".join(str(p + 1) for p in positions))

        ok = True
        for p in positions:
            print(f"  символ №{p + 1}: ", end="", flush=True)
            ch = read_char()
            print()
            if ch != password[p]:
                ok = False
        if ok:
            ts = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            save_timestamp(ts)
            print("\nДоступ разрешён. Добро пожаловать!")
            return True
        print("  Неверные символы!")
    print("\nИсчерпано число попыток. Доступ заблокирован.")
    return False


def main():
    random.seed()
    if not os.path.exists(PASS_FILE):
        setup_password()
    authenticate()


if __name__ == "__main__":
    main()
