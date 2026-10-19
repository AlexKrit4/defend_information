# -*- coding: utf-8 -*-
"""
Лабораторная работа № 5. Вариант 11.
Электронная цифровая подпись по ГОСТ Р34.10-94.
Хэш-функция (контрольная сумма по таблице 5.1, вариант 11):
    h(m) = произведение кодов символов исходного текста mod 2^16.

Алгоритм:
  p - простое, q - простой делитель (p-1), a: a^q = 1 (mod p), 1<a<p-1;
  x - секретный ключ (0<x<q),  y = a^x mod p - открытый ключ.
  Подпись:  r = (a^k mod p) mod q;  s = (x*r + k*h) mod q;  k - случайное.
  Проверка: v = h^(q-2) mod q;  z1 = s*v mod q;  z2 = (q-r)*v mod q;
            u = ((a^z1 * y^z2) mod p) mod q;  подпись верна, если u = r.
"""

import random

# --- параметры системы (учебные значения): q | (p-1), a^q = 1 (mod p) ---
P, Q, A = 2039, 1019, 100   # 2039 = 2*1019 + 1, оба простые; a = 10^2 mod p
X = 313                     # секретный ключ подписывающего
K = 77                      # одноразовое случайное число 0 < k < q


def hash_msg(text):
    """Вариант 11: произведение кодов символов по модулю 2^16."""
    h = 1
    for ch in text:
        h = (h * ord(ch)) % 65536
    return h


def sign(text, x, k):
    """Формирование подписи (r, s)."""
    h = hash_msg(text) % P
    if h == 0:
        h = 1
    while True:
        r = pow(A, k, P) % Q
        if r == 0:
            k = random.randrange(1, Q)
            continue
        s = (x * r + k * h) % Q
        if s == 0:
            k = random.randrange(1, Q)
            continue
        return r, s, h


def verify(text, r, s, y):
    """Проверка подписи."""
    if not (0 < r < Q and 0 < s < Q):
        return False
    h = hash_msg(text) % P
    if h == 0:
        h = 1
    v = pow(h, Q - 2, Q)                    # h^{-1} mod q (q - простое)
    z1 = (s * v) % Q
    z2 = ((Q - r) * v) % Q
    u = ((pow(A, z1, P) * pow(y, z2, P)) % P) % Q
    return u == r


def main():
    y = pow(A, X, P)
    print(f"Параметры: p={P}, q={Q}, a={A}; проверка a^q mod p = "
          f"{pow(A, Q, P)} (должно быть 1)")
    print(f"Секретный ключ x = {X}; открытый ключ y = a^x mod p = {y}")

    text = input("\nВведите подписываемый текст (напр. GOST11): ")
    h = hash_msg(text)
    print(f"Хэш сообщения h = {h} (умножение кодов mod 2^16)")

    r, s, _ = sign(text, X, K)
    print(f"Одноразовый ключ k = {K}")
    print(f"Подпись: r = {r}, s = {s}")

    ok = verify(text, r, s, y)
    print("\nПроверка ЭЦП:", "ПОДПИСЬ ПОДЛИННАЯ" if ok else "ПОДПИСЬ НЕВЕРНА")

    # п.5 задания: изменить подпись и убедиться, что она не подлинная
    s_bad = (s + 1) % Q
    ok_bad = verify(text, r, s_bad, y)
    print(f"\nИзменённая подпись: r = {r}, s' = {s_bad}")
    print("Проверка изменённой ЭЦП:",
          "ПОДПИСЬ ПОДЛИННАЯ" if ok_bad else "ПОДПИСЬ НЕВЕРНА")
    # также проверка при изменении текста
    text_bad = text[:-1] + ("2" if text[-1] != "2" else "3")
    ok_txt = verify(text_bad, r, s, y)
    print(f"Проверка подписи для изменённого текста '{text_bad}':",
          "ПОДПИСЬ ПОДЛИННАЯ" if ok_txt else "ПОДПИСЬ НЕВЕРНА")


if __name__ == "__main__":
    main()
