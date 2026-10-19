# -*- coding: utf-8 -*-
"""
Лабораторная работа № 2. Вариант 11.
Шифрование при помощи генератора псевдослучайных чисел.
Вид генератора: ЛИНЕЙНЫЙ КОНГРУЭНТНЫЙ датчик ПСЧ.
Количество разрядов b = 7  =>  модуль M = 2^7 = 128.

Линейный конгруэнтный генератор:  T(i) = (A*T(i-1) + C) mod M
Условия максимального периода (Кнут):
    C - нечётное;
    A mod 4 = 1  (т.к. M кратно 4);
    T(0) - начальное значение, 0 <= T(0) < M.

Гаммирование: каждый символ -> b-битный код,
C_i = M_i XOR T(i);  дешифрование - та же операция.
"""

B = 7                  # разрядность по варианту
M = 2 ** B             # модуль M = 128


def gamma(a, c, t0, n, m=M):
    """Линейный конгруэнтный генератор: n чисел последовательности."""
    seq, t = [], t0
    for _ in range(n):
        t = (a * t + c) % m
        seq.append(t)
    return seq


def crypt(text, gam):
    """Наложение гаммы: XOR кода символа с числом ПСЧ."""
    return [ord(ch) ^ g for ch, g in zip(text, gam)]


def to_bits(nums):
    return " ".join(f"{v:0{B}b}" for v in nums)


def main():
    text = input("Введите исходный текст (ASCII, коды < 128): ")
    for ch in text:
        assert ord(ch) < M, f"код символа '{ch}' >= {M}"

    # параметры генератора (условия Кнута: C нечётно, A mod 4 = 1)
    A, C, T0 = 29, 77, 11
    print(f"\nГенератор: T(i) = ({A}*T(i-1) + {C}) mod {M},  T(0) = {T0}")
    print(f"Проверка условий Кнута: C нечётно: {C % 2 == 1}; "
          f"A mod 4 = 1: {A % 4 == 1}")

    gam = gamma(A, C, T0, len(text))
    print("Гамма (ПСЧ):", gam)

    src = [ord(ch) for ch in text]
    print("\nКоды исходного текста:", src)
    print("       (двоичные):", to_bits(src))

    cipher = crypt(text, gam)
    print("\nКриптограмма (коды):", cipher)
    print("        (двоичные):", to_bits(cipher))
    print("        (символы):", "".join(map(chr, cipher)))

    back = "".join(map(chr, crypt("".join(map(chr, cipher)),
                                  gamma(A, C, T0, len(cipher)))))
    print("\nДешифрованный текст:", back)
    print("Совпадение с исходным:", back == text)

    # п.4 задания: изменение параметров генератора и сравнение криптограмм
    print("\n--- Изменение параметров генератора ---")
    A2, C2, T02 = 25, 51, 3
    gam2 = gamma(A2, C2, T02, len(text))
    cipher2 = crypt(text, gam2)
    print(f"Новые параметры: A={A2}, C={C2}, T(0)={T02}")
    print("Новая гамма:        ", gam2)
    print("Новая криптограмма: ", cipher2)
    same = sum(x == y for x, y in zip(cipher, cipher2))
    print(f"Совпало байтов криптограмм: {same} из {len(cipher)} "
          f"-> криптограммы различны")


if __name__ == "__main__":
    main()
