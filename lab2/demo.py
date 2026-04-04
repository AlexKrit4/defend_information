"""
Быстрая демонстрация RSA
Запустить: python demo.py
"""

from rsa import RSA


def demo():
    """Быстрая демонстрация"""
    print("\n" + "=" * 70)
    print("RSA ШАГ ЗА ШАГОМ")
    print("=" * 70)
    
    # Создаем RSA
    print("\n1️⃣ СОЗДАНИЕ КЛЮЧЕЙ")
    print("-" * 70)
    rsa = RSA(p=7, q=13, e=5)
    
    # Параметры
    print(f"\n2️⃣ ПАРАМЕТРЫ")
    print("-" * 70)
    print(f"p = 7, q = 13")
    print(f"n = p × q = {rsa.n}")
    print(f"φ(n) = (p-1) × (q-1) = {rsa.phi}")
    print(f"e = 5")
    print(f"d = 29")
    
    # Таблица кодирования
    print(f"\n3️⃣ ТАБЛИЦА КОДИРОВАНИЯ")
    print("-" * 70)
    message = "КАФСИ"
    codes = rsa.encode_text(message)
    for char, code in zip(message, codes):
        print(f"{char:3} → {code:2d}")
    
    # Шифрование
    print(f"\n4️⃣ ШИФРОВАНИЕ (C = T^e mod n)")
    print("-" * 70)
    encrypted = []
    for char, code in zip(message, codes):
        enc = pow(code, rsa.e, rsa.n)
        encrypted.append(enc)
        print(f"{char} ({code:2d}): {code}^{rsa.e} mod {rsa.n} = {enc:2d}")
    
    print(f"\nШифрограмма: {encrypted}")
    
    # Расшифрование
    print(f"\n5️⃣ РАСШИФРОВАНИЕ (T = C^d mod n)")
    print("-" * 70)
    decrypted = []
    for code in encrypted:
        dec = pow(code, rsa.d, rsa.n)
        decrypted.append(dec)
        print(f"{code:2d}: {code}^{rsa.d} mod {rsa.n} = {dec:2d}")
    
    recovered = rsa.decode_text(decrypted)
    print(f"\nВосстановленное: {recovered}")
    
    # Проверка
    print(f"\n6️⃣ ПРОВЕРКА")
    print("-" * 70)
    if message == recovered:
        print(f"✅ Исходное:      {message}")
        print(f"✅ Восстановлено: {recovered}")
        print(f"✅ СОВПАДАЕТ!")
    else:
        print(f"❌ Не совпадает!")


def compare_two_messages():
    """Сравнивает два разных сообщения"""
    print("\n" + "=" * 70)
    print("СРАВНЕНИЕ: КАФСИ vs ЗАЩИТА")
    print("=" * 70)
    
    rsa = RSA(p=61, q=53, e=17)
    
    messages = ["КАФСИ", "ЗАЩИТА"]
    
    for msg in messages:
        print(f"\nСообщение: {msg}")
        encrypted = rsa.encrypt(msg)
        print(f"Шифрограмма: {encrypted}")
        decrypted = rsa.decrypt(encrypted)
        print(f"Восстановлено: {decrypted} {'✅' if msg == decrypted else '❌'}")


def show_formula_sheet():
    """Показывает лист формул"""
    print("\n" + "=" * 70)
    print("ФОРМУЛЫ RSA")
    print("=" * 70)
    
    formulas = """
    ГЕНЕРАЦИЯ КЛЮЧЕЙ:
    ─────────────────
    1. n = p × q
    2. φ(n) = (p-1) × (q-1)
    3. gcd(e, φ(n)) = 1
    4. (d × e) mod φ(n) = 1
    
    ШИФРОВАНИЕ:
    ───────────
    C = T^e mod n
    где:
      T - числовой код открытого текста
      C - числовой код шифротекста
      e - открытая экспонента
      n - общий модуль
    
    РАСШИФРОВАНИЕ:
    ──────────────
    T = C^d mod n
    где:
      C - числовой код шифротекста
      T - числовой код открытого текста
      d - закрытая экспонента
      n - общий модуль
    
    ПРИМЕР ВЫЧИСЛЕНИЯ d:
    ────────────────────
    d = (1 + k × φ(n)) / e
    где k подбирается так, чтобы d было целым числом
    и выполнялось: (d × e) mod φ(n) = 1
    
    При k=1: d = (1 + 1×72) / 5 = 73/5 = 14.6 (не целое)
    При k=2: d = (1 + 2×72) / 5 = 145/5 = 29 ✓
    
    ПРОВЕРКА d:
    ──────────
    (29 × 5) mod 72 = 145 mod 72 = 1 ✓
    """
    
    print(formulas)


if __name__ == "__main__":
    demo()
    show_formula_sheet()
    compare_two_messages()
