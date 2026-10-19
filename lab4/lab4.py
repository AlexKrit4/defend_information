# -*- coding: utf-8 -*-
"""
Лабораторная работа № 4. Вариант 11.
Криптосистема с открытым ключом RSA.

1) выбираются простые p, q; n = p*q;  phi(n) = (p-1)(q-1);
2) e - взаимно просто с phi(n);  (e,n) - открытый ключ;
3) d: (e*d) mod phi(n) = 1;      (d,n) - секретный ключ;
4) C(i) = M(i)^e mod n;   M(i) = C(i)^d mod n.
Длина сообщения M >= 2*вариант = 22 символа.
Криптограмма сохраняется в отдельный файл cipher.txt.
В программе предусмотрена проверка взаимной простоты двух чисел (НОД).
"""

import random
import math
import os

CIPHER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "cipher.txt")


def is_prime(n, rounds=16):
    """Проверка простоты (Миллер-Рабин)."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits=16):
    """Генерация простого числа заданной разрядности."""
    while True:
        n = random.randrange(2 ** (bits - 1) | 1, 2 ** bits)
        if is_prime(n):
            return n


def egcd(a, b):
    """Расширенный алгоритм Евклида: (НОД, x, y): a*x + b*y = НОД."""
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def coprime(a, b):
    """Проверка взаимной простоты двух чисел."""
    return math.gcd(a, b) == 1


def mod_inverse(e, phi):
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("e и phi(n) не взаимно просты")
    return x % phi


def main():
    random.seed()

    # --- генерация ключей ---
    p = gen_prime(16)
    q = gen_prime(16)
    while q == p:
        q = gen_prime(16)
    n = p * q
    phi = (p - 1) * (q - 1)

    print("p =", p, "- простое:", is_prime(p))
    print("q =", q, "- простое:", is_prime(q))
    print("n = p*q =", n)
    print("phi(n) = (p-1)(q-1) =", phi)

    e = random.randrange(3, phi, 2)
    while not coprime(e, phi):
        e = random.randrange(3, phi, 2)
    d = mod_inverse(e, phi)
    print("\nПроверка взаимной простоты e и phi(n): "
          f"gcd({e}, {phi}) = {math.gcd(e, phi)} -> взаимно просты")
    print(f"Открытый ключ  (e, n) = ({e}, {n})")
    print(f"Секретный ключ (d, n) = ({d}, {n})")
    print(f"Контроль: (e*d) mod phi(n) = {(e * d) % phi}")

    # --- проверка взаимной простоты двух произвольных чисел ---
    try:
        a, b = map(int, input("\nПроверка взаимной простоты - "
                              "введите два числа через пробел: ").split())
        print(f"gcd({a}, {b}) = {math.gcd(a, b)} ->",
              "взаимно простые" if coprime(a, b) else "НЕ взаимно простые")
    except ValueError:
        print("пропущено")

    # --- шифрование ---
    text = input("\nВведите сообщение M (>= 22 символов): ").strip()
    assert len(text) >= 22, "сообщение короче 22 символов"
    assert max(map(ord, text)) < n, "n слишком мало для кодов символов"

    m_codes = [ord(ch) for ch in text]
    c_codes = [pow(m, e, n) for m in m_codes]
    with open(CIPHER_FILE, "w", encoding="utf-8") as f:
        f.write(" ".join(map(str, c_codes)))
    print(f"\nКриптограмма записана в файл: {CIPHER_FILE}")
    print("C(i):", c_codes)

    # --- дешифрование из файла ---
    with open(CIPHER_FILE, encoding="utf-8") as f:
        c_read = [int(x) for x in f.read().split()]
    restored = "".join(chr(pow(c, d, n)) for c in c_read)
    print("\nДешифрованный текст:", restored)
    print("Совпадение с исходным:", restored == text)


if __name__ == "__main__":
    main()
