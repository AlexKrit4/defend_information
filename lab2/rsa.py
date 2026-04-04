"""
RSA Encryption/Decryption module
Защита информации - Лабораторная работа №2
"""

from math import gcd


class RSA:
    """Класс для работы с RSA шифром"""
    
    # Таблица кодирования русских букв, цифр и пробела
    # Русские буквы А-Я (1-33), пробел (34), цифры 0-9 (35-44)
    ENCODE_TABLE = {
        'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8,
        'З': 9, 'И': 10, 'Й': 11, 'К': 12, 'Л': 13, 'М': 14, 'Н': 15, 'О': 16,
        'П': 17, 'Р': 18, 'С': 19, 'Т': 20, 'У': 21, 'Ф': 22, 'Х': 23, 'Ц': 24,
        'Ч': 25, 'Ш': 26, 'Щ': 27, 'Ъ': 28, 'Ы': 29, 'Ь': 30, 'Э': 31, 'Ю': 32,
        'Я': 33, ' ': 34, '0': 35, '1': 36, '2': 37, '3': 38, '4': 39, '5': 40,
        '6': 41, '7': 42, '8': 43, '9': 44
    }
    
    # Обратная таблица для декодирования
    DECODE_TABLE = {v: k for k, v in ENCODE_TABLE.items()}
    
    def __init__(self, p=None, q=None, e=None):
        """
        Инициализация RSA с двумя простыми числами p и q
        
        Args:
            p: первое простое число
            q: второе простое число
            e: открытая экспонента
        """
        if p is None or q is None:
            raise ValueError("Необходимо указать два простых числа p и q")
        
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        
        if e is None:
            # Если e не указана, выбираем 65537 (стандартное значение)
            self.e = self._select_e()
        else:
            # Проверяем что e взаимно простая с φ(n)
            if gcd(e, self.phi) != 1:
                raise ValueError(f"e={e} не взаимно простая с φ(n)={self.phi}")
            self.e = e
        
        # Вычисляем закрытый ключ d
        self.d = self._compute_d()
        
        print(f"✓ RSA ключи созданы")
        print(f"  p = {self.p}, q = {self.q}")
        print(f"  n = {self.n}, φ(n) = {self.phi}")
        print(f"  Открытый ключ (e, n) = ({self.e}, {self.n})")
        print(f"  Закрытый ключ (d, n) = ({self.d}, {self.n})")
        print()
    
    def _select_e(self):
        """Выбирает подходящее значение e для φ(n)"""
        # Попробуем стандартные значения
        candidates = [65537, 17, 13, 7, 5, 3]
        for candidate in candidates:
            if candidate < self.n and gcd(candidate, self.phi) == 1:
                return candidate
        
        # Если стандартные не подходят, ищем первое подходящее нечетное число
        for e in range(3, self.phi, 2):
            if gcd(e, self.phi) == 1:
                return e
        
        raise ValueError("Не удалось найти подходящее e для данных p и q")
    
    def _compute_d(self):
        """
        Вычисляет закрытый ключ d из соотношения:
        (d * e) mod φ(n) = 1
        
        Используется формула: d = (1 + k * φ(n)) / e
        где k подбирается так чтобы d было целым числом
        """
        k = 1
        while True:
            numerator = 1 + k * self.phi
            if numerator % self.e == 0:
                d = numerator // self.e
                # Проверяем корректность
                if (d * self.e) % self.phi == 1:
                    return d
            k += 1
            
            # Предохранение от бесконечного цикла (не должно быть)
            if k > 10000:
                raise ValueError(f"Не удалось найти d для e={self.e}")
    
    def is_prime(self, num):
        """Проверка числа на простоту (простая реализация)"""
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def encode_text(self, text):
        """Преобразует текст в список числовых кодов"""
        codes = []
        text = text.upper()
        for char in text:
            if char in self.ENCODE_TABLE:
                codes.append(self.ENCODE_TABLE[char])
            else:
                print(f"⚠ Символ '{char}' не поддерживается, пропускаем")
        return codes
    
    def decode_text(self, codes):
        """Преобразует список числовых кодов в текст"""
        text = ""
        for code in codes:
            if code in self.DECODE_TABLE:
                text += self.DECODE_TABLE[code]
            else:
                text += f"[{code}]"
        return text
    
    def encrypt(self, message):
        """
        Шифрует сообщение открытым ключом
        Формула: C = T^e mod n
        
        Args:
            message: текст сообщения
            
        Returns:
            список зашифрованных кодов
        """
        text_codes = self.encode_text(message)
        encrypted = []
        
        for code in text_codes:
            # Применяем формулу RSA шифрования
            encrypted_code = pow(code, self.e, self.n)
            encrypted.append(encrypted_code)
        
        return encrypted
    
    def decrypt(self, encrypted):
        """
        Расшифровывает сообщение закрытым ключом
        Формула: T = C^d mod n
        
        Args:
            encrypted: список зашифрованных кодов
            
        Returns:
            исходный текст сообщения
        """
        decrypted_codes = []
        
        for code in encrypted:
            # Применяем формулу RSA расшифрования
            decrypted_code = pow(code, self.d, self.n)
            decrypted_codes.append(decrypted_code)
        
        message = self.decode_text(decrypted_codes)
        return message
    
    def get_public_key(self):
        """Возвращает открытый ключ"""
        return (self.e, self.n)
    
    def get_private_key(self):
        """Возвращает закрытый ключ"""
        return (self.d, self.n)


def test_example():
    """Тестирует пример из лабораторной работы"""
    print("=" * 60)
    print("ТЕСТ: Пример из лабораторной работы")
    print("=" * 60)
    print()
    
    # Создаем RSA с параметрами из примера
    rsa = RSA(p=7, q=13, e=5)
    
    # Исходное сообщение
    message = "КАФСИ"
    print(f"Исходное сообщение: {message}")
    print()
    
    # Кодирование символов
    print("Кодирование символов:")
    text_codes = rsa.encode_text(message)
    for char, code in zip(message, text_codes):
        print(f"  {char} -> {code}")
    print()
    
    # Шифрование
    print("Шифрование (C = T^e mod n, где e=5, n=91):")
    encrypted = rsa.encrypt(message)
    for char, code, enc in zip(message, text_codes, encrypted):
        print(f"  {char} ({code}) -> {code}^5 mod 91 = {enc}")
    print(f"Шифрограмма: {encrypted}")
    print()
    
    # Расшифрование
    print("Расшифрование (T = C^d mod n, где d=29, n=91):")
    decrypted = rsa.decrypt(encrypted)
    for enc, dec_code in zip(encrypted, rsa.encode_text(decrypted)):
        print(f"  {enc} -> {enc}^29 mod 91 = {dec_code}")
    print(f"Восстановленное сообщение: {decrypted}")
    print()
    
    # Проверка
    if message == decrypted:
        print("✅ Тест пройден! Сообщение успешно восстановлено")
    else:
        print("❌ Тест не пройден!")
    print()


if __name__ == "__main__":
    test_example()
