"""
Тесты и примеры использования RSA
Защита информации - Лабораторная работа №2
"""

from rsa import RSA


def test_lab_example():
    """Тест: Пример из лабораторной работы - КАФСИ"""
    print("\n" + "=" * 70)
    print("ТЕСТ 1: Пример из лабораторной работы")
    print("=" * 70)
    
    print("\nСоздание ключей: p=7, q=13, e=5")
    rsa = RSA(p=7, q=13, e=5)
    
    message = "КАФСИ"
    print(f"\nИсходное сообщение: {message}")
    
    # Показываем процесс кодирования
    print("\nТаблица 1: Кодирование символов")
    print("Символ | Код | Зашифрованный код")
    print("--------|-----|------------------")
    
    codes = rsa.encode_text(message)
    encrypted = rsa.encrypt(message)
    
    for char, code, enc_code in zip(message, codes, encrypted):
        print(f"   {char}    |  {code:2d}  |      {enc_code:2d}")
    
    print(f"\nШифрограмма: {', '.join(map(str, encrypted))}")
    
    # Показываем процесс расшифрования
    print("\nТаблица 2: Расшифрование")
    print("Закодированный | Декодированный | Символ")
    print("     код       |      код       |")
    print("---------------|----------------|--------")
    
    decrypted_codes = []
    for enc_code in encrypted:
        dec_code = pow(enc_code, rsa.d, rsa.n)
        decrypted_codes.append(dec_code)
    
    for enc_code, dec_code, char in zip(encrypted, decrypted_codes, message):
        print(f"      {enc_code:2d}       |       {dec_code:2d}       |   {char}")
    
    decrypted = rsa.decrypt(encrypted)
    print(f"\nВосстановленное сообщение: {decrypted}")
    
    if message == decrypted:
        print("✅ ТЕСТ ПРОЙДЕН!")
        return True
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
        return False


def test_long_message():
    """Тест: Длинное сообщение"""
    print("\n" + "=" * 70)
    print("ТЕСТ 2: Длинное сообщение")
    print("=" * 70)
    
    # Используем другие параметры для большего n
    print("\nСоздание ключей: p=61, q=53, e=17")
    rsa = RSA(p=61, q=53, e=17)
    
    message = "ЗАЩИТА ИНФОРМАЦИИ"
    print(f"\nИсходное сообщение: {message}")
    
    encrypted = rsa.encrypt(message)
    print(f"Шифрограмма: {encrypted}")
    
    decrypted = rsa.decrypt(encrypted)
    print(f"Восстановленное: {decrypted}")
    
    if message == decrypted:
        print("✅ ТЕСТ ПРОЙДЕН!")
        return True
    else:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
        return False


def test_single_char():
    """Тест: Одиночные символы"""
    print("\n" + "=" * 70)
    print("ТЕСТ 3: Шифрование отдельных символов")
    print("=" * 70)
    
    print("\nСоздание ключей: p=7, q=13, e=5")
    rsa = RSA(p=7, q=13, e=5)
    
    test_chars = ['А', 'К', 'Я', ' ', '0', '9']
    
    print("\nШифрование отдельных символов:")
    for char in test_chars:
        if char in rsa.ENCODE_TABLE:
            code = rsa.ENCODE_TABLE[char]
            encrypted_code = pow(code, rsa.e, rsa.n)
            decrypted_code = pow(encrypted_code, rsa.d, rsa.n)
            decrypted_char = rsa.DECODE_TABLE[decrypted_code]
            
            status = "✓" if char == decrypted_char else "✗"
            print(f"  {status} '{char}' -> {code:2d} -> {encrypted_code:2d} -> {decrypted_code:2d} -> '{decrypted_char}'")


def test_empty_message():
    """Тест: Обработка специальных случаев"""
    print("\n" + "=" * 70)
    print("ТЕСТ 4: Обработка специальных случаев")
    print("=" * 70)
    
    print("\nСоздание ключей: p=7, q=13, e=5")
    rsa = RSA(p=7, q=13, e=5)
    
    # Тест с разными строками
    test_messages = [
        "АБВ",
        "123",
        "АБВ 123",
    ]
    
    print("\nТестирование разных сообщений:")
    for message in test_messages:
        encrypted = rsa.encrypt(message)
        decrypted = rsa.decrypt(encrypted)
        status = "✓" if message == decrypted else "✗"
        print(f"  {status} '{message}' -> {encrypted} -> '{decrypted}'")


def test_key_generation():
    """Тест: Проверка вычисления ключей"""
    print("\n" + "=" * 70)
    print("ТЕСТ 5: Проверка вычисления ключей")
    print("=" * 70)
    
    p, q, e = 7, 13, 5
    print(f"\nПараметры: p={p}, q={q}, e={e}")
    
    rsa = RSA(p=p, q=q, e=e)
    
    # Проверяем основные свойства
    print("\nПроверка свойств:")
    
    # n = p*q
    expected_n = p * q
    status = "✓" if rsa.n == expected_n else "✗"
    print(f"  {status} n = p*q => {rsa.n} = {expected_n}")
    
    # φ(n) = (p-1)*(q-1)
    expected_phi = (p - 1) * (q - 1)
    status = "✓" if rsa.phi == expected_phi else "✗"
    print(f"  {status} φ(n) = (p-1)*(q-1) => {rsa.phi} = {expected_phi}")
    
    # gcd(e, φ(n)) = 1
    from math import gcd
    expected_gcd = gcd(rsa.e, rsa.phi)
    status = "✓" if expected_gcd == 1 else "✗"
    print(f"  {status} gcd(e, φ(n)) = 1 => {expected_gcd} = 1")
    
    # (d*e) mod φ(n) = 1
    check = (rsa.d * rsa.e) % rsa.phi
    status = "✓" if check == 1 else "✗"
    print(f"  {status} (d*e) mod φ(n) = 1 => {check} = 1")
    
    print(f"\nОткрытый ключ (e, n) = ({rsa.e}, {rsa.n})")
    print(f"Закрытый ключ (d, n) = ({rsa.d}, {rsa.n})")


def run_all_tests():
    """Запустить все тесты"""
    print("\n" + "=" * 70)
    print("    ЗАПУСК ВСЕХ ТЕСТОВ RSA")
    print("=" * 70)
    
    tests = [
        test_key_generation,
        test_lab_example,
        test_single_char,
        test_long_message,
        test_empty_message,
    ]
    
    passed = 0
    total = 0
    
    for test in tests:
        try:
            result = test()
            total += 1
            if result is not False:
                passed += 1
        except Exception as e:
            print(f"\n❌ Ошибка при выполнении теста: {e}")
            total += 1
    
    print("\n" + "=" * 70)
    print(f"РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
