#!/usr/bin/env python3
"""
Примеры RSA из лабораторной работы
Точное повторение примера из задания
"""

from rsa import RSA


def example_from_lab():
    """
    Точный пример из лабораторной работы:
    Сообщение "КАФСИ", параметры p=7, q=13, e=5
    """
    print("\n" + "=" * 80)
    print("ПРИМЕР ИЗ ЛАБОРАТОРНОЙ РАБОТЫ №2")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("ЭТАП 1: ГЕНЕРАЦИЯ КЛЮЧЕЙ")
    print("=" * 80)
    
    p = 7
    q = 13
    e = 5
    
    print(f"\n1. Выбрали два простых числа:")
    print(f"   p = {p}")
    print(f"   q = {q}")
    
    n = p * q
    print(f"\n2. Вычислили n = p × q:")
    print(f"   n = {p} × {q} = {n}")
    
    phi = (p - 1) * (q - 1)
    print(f"\n3. Вычислили φ(n) = (p-1) × (q-1):")
    print(f"   φ(n) = ({p}-1) × ({q}-1) = {p-1} × {q-1} = {phi}")
    
    print(f"\n4. Выбрали открытую экспоненту e:")
    print(f"   e = {e}")
    print(f"   (она взаимно простая с φ(n) = {phi})")
    
    print(f"\n5. Вычислили закрытую экспоненту d:")
    print(f"   Используем формулу: d = (1 + k×φ(n)) / e")
    
    k = 1
    d = None
    while d is None:
        numerator = 1 + k * phi
        if numerator % e == 0:
            d_candidate = numerator // e
            # Проверяем что (d*e) mod φ(n) = 1
            if (d_candidate * e) % phi == 1:
                print(f"   При k = {k}: d = (1 + {k}×{phi}) / {e} = {numerator} / {e} = {d_candidate}")
                d = d_candidate
                break
        else:
            print(f"   При k = {k}: d = (1 + {k}×{phi}) / {e} = {numerator} / {e} — не целое")
        k += 1
    
    print(f"\n   Проверка: (d × e) mod φ(n) = ({d} × {e}) mod {phi} = {(d*e) % phi}")
    
    print(f"\nРЕЗУЛЬТАТ:")
    print(f"  Открытый ключ (e, n) = ({e}, {n})")
    print(f"  Закрытый ключ (d, n) = ({d}, {n})")
    
    # Создаем объект RSA с этими параметрами
    rsa = RSA(p=p, q=q, e=e)
    
    # Проверка что d совпадает
    assert rsa.d == d, "Вычисленное d не совпадает!"
    
    print("\n" + "=" * 80)
    print("ЭТАП 2: ШИФРОВАНИЕ СООБЩЕНИЯ «КАФСИ»")
    print("=" * 80)
    
    message = "КАФСИ"
    print(f"\nИсходное сообщение: {message}")
    
    print(f"\nТаблица кодирования символов:")
    codes = rsa.encode_text(message)
    for char, code in zip(message, codes):
        print(f"  {char} → {code}")
    
    print(f"\nШифрование каждого символа по формуле C = T^e mod n:")
    print(f"(где e = {e}, n = {n})")
    print()
    
    print("Символ | Код символа | Вычисление | Результат")
    print("--------|-------------|-----------|----------")
    
    encrypted = []
    for char, code in zip(message, codes):
        encrypted_code = pow(code, e, n)
        encrypted.append(encrypted_code)
        print(f"  {char}    |      {code:2d}      | {code}^{e} mod {n} = {encrypted_code:2d}")
    
    print(f"\nШифрограмма: {', '.join(map(str, encrypted))}")
    
    print("\n" + "=" * 80)
    print("ЭТАП 3: РАСШИФРОВАНИЕ СООБЩЕНИЯ")
    print("=" * 80)
    
    print(f"\nШифрограмма: {', '.join(map(str, encrypted))}")
    
    print(f"\nРасшифрование каждого символа по формуле T = C^d mod n:")
    print(f"(где d = {d}, n = {n})")
    print()
    
    print("Зашифр. код | Вычисление | Код символа | Символ")
    print("------------|-----------|-------------|--------")
    
    decrypted_codes = []
    for encrypted_code in encrypted:
        decrypted_code = pow(encrypted_code, d, n)
        decrypted_codes.append(decrypted_code)
        char = rsa.DECODE_TABLE[decrypted_code]
        print(f"     {encrypted_code:2d}      | {encrypted_code}^{d} mod {n} |      {decrypted_code:2d}      |  {char}")
    
    decrypted = rsa.decode_text(decrypted_codes)
    
    print(f"\nВосстановленное сообщение: {decrypted}")
    
    print("\n" + "=" * 80)
    print("ПРОВЕРКА")
    print("=" * 80)
    
    if message == decrypted:
        print(f"\n✅ УСПЕХ!")
        print(f"Исходное:      {message}")
        print(f"Расшифровано:  {decrypted}")
        print(f"Совпадают!")
    else:
        print(f"\n❌ ОШИБКА!")
        print(f"Исходное:      {message}")
        print(f"Расшифровано:  {decrypted}")


def detailed_key_generation():
    """
    Подробное объяснение генерации ключей
    """
    print("\n" + "=" * 80)
    print("ПОДРОБНОЕ ОБЪЯСНЕНИЕ ГЕНЕРАЦИИ КЛЮЧЕЙ")
    print("=" * 80)
    
    print("""
    Алгоритм генерации RSA ключей:
    
    1. ВЫБОР ПРОСТЫХ ЧИСЕЛ (p и q)
       - Выбираем два больших простых числа (в реальности 1024+ бит)
       - В примере используем малые: p=7, q=13
       - Чем больше p и q, тем более стойкий шифр
    
    2. ВЫЧИСЛЕНИЕ n
       - n = p × q = 7 × 13 = 91
       - n используется в обоих ключах (открытом и закрытом)
       - Сложность разложения n на p и q определяет стойкость RSA
    
    3. ВЫЧИСЛЕНИЕ ФУНКЦИИ ЭЙЛЕРА φ(n)
       - φ(n) = (p-1) × (q-1)
       - φ(n) = 6 × 12 = 72
       - Это количество целых чисел <= n, взаимно простых с n
       - Используется для вычисления приватного ключа
    
    4. ВЫБОР ОТКРЫТОЙ ЭКСПОНЕНТЫ e
       - e должна быть взаимно простой с φ(n)
       - Чаще всего e = 65537 (в реальных системах)
       - В примере e = 5
       - gcd(5, 72) = 1 ✓ (значит e подходит)
    
    5. ВЫЧИСЛЕНИЕ ЗАКРЫТОЙ ЭКСПОНЕНТЫ d
       - Решаем уравнение: (d × e) mod φ(n) = 1
       - Используем расширенный алгоритм Евклида или перебор
       - Формула: d = (1 + k×φ(n)) / e, k = 1, 2, 3, ...
       - При k=2: d = (1 + 144) / 5 = 29
       - Проверка: (29 × 5) mod 72 = 145 mod 72 = 1 ✓
    
    РЕЗУЛЬТАТЫ:
       - Открытый ключ (e, n) = (5, 91)  — передается всем
       - Закрытый ключ (d, n) = (29, 91) — держится в тайне
    """)


def mathematical_explanation():
    """
    Математическое объяснение RSA
    """
    print("\n" + "=" * 80)
    print("МАТЕМАТИЧЕСКОЕ ОБЪЯСНЕНИЕ RSA")
    print("=" * 80)
    
    print("""
    ПОЧЕМУ RSA РАБОТАЕТ?
    
    Основано на теореме Эйлера:
    Если gcd(a, n) = 1, то a^φ(n) ≡ 1 (mod n)
    
    Это означает:
    - Если y = x^e mod n (зашифровали)
    - То x = y^d mod n (расшифровали)
    
    При условии: (d × e) ≡ 1 (mod φ(n))
    
    Доказательство:
    Пусть e × d = 1 + k × φ(n) для некоторого k
    
    Тогда:
    y^d = (x^e)^d = x^(e×d) = x^(1+k×φ(n)) mod n
        = x × x^(k×φ(n)) mod n
        = x × (x^φ(n))^k mod n
        = x × 1^k mod n   (по теореме Эйлера)
        = x mod n
    
    ПРИМЕР:
    x = 12 (символ К)
    e = 5, d = 29, n = 91, φ(n) = 72
    
    Проверка что (e × d) mod φ(n) = 1:
    (5 × 29) mod 72 = 145 mod 72 = 1 ✓
    
    Шифрование:
    y = 12^5 mod 91 = 248832 mod 91 = 38
    
    Расшифрование:
    x = 38^29 mod 91 = ... (большое число) ... = 12 ✓
    
    ПОЧЕМУ БЕЗОПАСНО?
    - Зная (e, n), очень сложно найти (d, n)
    - Нужно разложить n на p и q (факторизация)
    - С большими простыми числами (1024+ бит) - вычислительно невозможно
    - С малыми числами (как в примере) - легко взломать
    """)


def encoding_table_explanation():
    """
    Объяснение таблицы кодирования
    """
    print("\n" + "=" * 80)
    print("ТАБЛИЦА КОДИРОВАНИЯ РУССКОГО ТЕКСТА")
    print("=" * 80)
    
    rsa = RSA(p=7, q=13)
    
    print("\nРусские буквы (1-33):")
    for i in range(1, 34):
        char = rsa.DECODE_TABLE.get(i, '?')
        if i % 10 == 1:
            print()
        print(f"{i:2d}:{char} ", end="")
    
    print("\n\nСпециальные символы (34-44):")
    for i in range(34, 45):
        char = rsa.DECODE_TABLE.get(i, '?')
        if char == ' ':
            print(f"{i:2d}:(пробел) ", end="")
        else:
            print(f"{i:2d}:{char} ", end="")
    
    print("\n\nПримеры кодирования:")
    test_words = ['КАФСИ', 'ЗАЩИТА', 'ИНФОРМАЦИЯ', 'КЛЮЧ']
    for word in test_words:
        codes = rsa.encode_text(word)
        print(f"  {word:12} → {codes}")


if __name__ == "__main__":
    # Запускаем основной пример
    example_from_lab()
    
    # Дополнительные объяснения
    input("\nНажмите Enter для продолжения...")
    detailed_key_generation()
    
    input("\nНажмите Enter для продолжения...")
    mathematical_explanation()
    
    input("\nНажмите Enter для просмотра таблицы кодирования...")
    encoding_table_explanation()
    
    print("\n" + "=" * 80)
    print("Конец работы")
    print("=" * 80 + "\n")
