"""
Интерактивная программа для RSA шифрования
Защита информации - Лабораторная работа №2
"""

from rsa import RSA


def print_menu():
    """Выводит меню программы"""
    print("\n" + "=" * 60)
    print("    RSA ШИФР - Интерактивное меню")
    print("=" * 60)
    print("1. Создать новую пару ключей")
    print("2. Использовать пример из лабораторной работы")
    print("3. Зашифровать сообщение")
    print("4. Расшифровать сообщение")
    print("5. Показать таблицу кодирования")
    print("6. Выход")
    print("=" * 60)


def print_encoding_table():
    """Выводит таблицу кодирования"""
    print("\n" + "=" * 60)
    print("Таблица кодирования символов")
    print("=" * 60)
    
    table = RSA.ENCODE_TABLE
    
    # Русские буквы
    print("\nРусские буквы (А-Я):")
    for i in range(1, 34):
        for char, code in table.items():
            if code == i and char != ' ' and not char.isdigit():
                print(f"  {i:2d}: {char}")
                break
    
    # Специальные символы
    print("\nСпециальные символы:")
    print(f"  34: <пробел>")
    
    # Цифры
    print("\nЦифры (0-9):")
    for i in range(35, 45):
        for char, code in table.items():
            if code == i and char.isdigit():
                print(f"  {i:2d}: {char}")
                break


def input_p_q():
    """Получает от пользователя два простых числа"""
    print("\n⚠ Введите два простых числа для создания ключей")
    
    while True:
        try:
            p = int(input("Введите p: "))
            if p < 2:
                print("❌ p должно быть >= 2")
                continue
            
            q = int(input("Введите q: "))
            if q < 2:
                print("❌ q должно быть >= 2")
                continue
            
            if p == q:
                print("❌ p и q должны быть разными")
                continue
            
            print(f"\n✓ Выбраны p={p}, q={q}")
            return p, q
        
        except ValueError:
            print("❌ Введите целые числа")


def input_e(phi):
    """Получает от пользователя открытую экспоненту e"""
    print(f"\nВведите e (должна быть взаимно простая с φ(n)={phi}):")
    print("Рекомендуемые значения: 3, 5, 7, 13, 17, 65537")
    
    while True:
        try:
            e = int(input("Введите e (или нажмите Enter для автовыбора): ") or "0")
            
            if e == 0:
                return None
            
            if e < 1:
                print("❌ e должна быть >= 1")
                continue
            
            return e
        
        except ValueError:
            print("❌ Введите целое число")


def main():
    """Главная функция программы"""
    print("\n" + "=" * 60)
    print("    Добро пожаловать в программу RSA!")
    print("=" * 60)
    
    rsa = None
    
    while True:
        print_menu()
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == "1":
            # Создать новую пару ключей
            print()
            p, q = input_p_q()
            print(f"\nфи(n) = (p-1)*(q-1) = ({p}-1)*({q}-1) = {(p-1)*(q-1)}")
            
            e = input_e((p-1)*(q-1))
            
            try:
                rsa = RSA(p=p, q=q, e=e)
            except ValueError as ex:
                print(f"❌ Ошибка: {ex}")
                rsa = None
        
        elif choice == "2":
            # Пример из лабораторной работы
            print()
            print("Используются параметры из лабораторной работы:")
            print("p=7, q=13, e=5")
            rsa = RSA(p=7, q=13, e=5)
            
            # Сразу показываем пример
            message = "КАФСИ"
            print(f"Исходное сообщение: {message}")
            
            encrypted = rsa.encrypt(message)
            print(f"Зашифрованное: {encrypted}")
            
            decrypted = rsa.decrypt(encrypted)
            print(f"Расшифрованное: {decrypted}")
            
            if message == decrypted:
                print("✅ Проверка пройдена!")
            else:
                print("❌ Проверка не пройдена!")
        
        elif choice == "3":
            # Зашифровать
            if rsa is None:
                print("\n❌ Сначала создайте или выберите ключи (пункт 1 или 2)")
                continue
            
            message = input("\nВведите сообщение для зашифрования: ").upper()
            
            if not message:
                print("❌ Сообщение не может быть пустым")
                continue
            
            print(f"\nКодирование: {message}")
            codes = rsa.encode_text(message)
            print(f"Коды: {codes}")
            
            print(f"\nШифрование (C = T^{rsa.e} mod {rsa.n}):")
            encrypted = rsa.encrypt(message)
            print(f"Шифрограмма: {encrypted}")
            
            # Сохраняем для последующего расшифрования
            print(f"\n✓ Сообщение зашифровано (скопируйте для расшифрования)")
        
        elif choice == "4":
            # Расшифровать
            if rsa is None:
                print("\n❌ Сначала создайте или выберите ключи (пункт 1 или 2)")
                continue
            
            print("\nВведите шифрованное сообщение (числа через запятую):")
            try:
                encrypted_str = input("Шифрограмма: ")
                encrypted = [int(x.strip()) for x in encrypted_str.split(',')]
                
                print(f"\nРасшифрование (T = C^{rsa.d} mod {rsa.n}):")
                decrypted = rsa.decrypt(encrypted)
                print(f"Восстановленное сообщение: {decrypted}")
            
            except ValueError:
                print("❌ Некорректный формат. Используйте: число1, число2, число3, ...")
        
        elif choice == "5":
            # Показать таблицу
            print_encoding_table()
        
        elif choice == "6":
            # Выход
            print("\n👋 До свидания!")
            break
        
        else:
            print("❌ Неважный выбор")


if __name__ == "__main__":
    main()
