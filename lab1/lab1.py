# -*- coding: utf-8 -*-
r"""
Лабораторная работа № 1. Вариант 11.
Шифрование методом ПЕРЕСТАНОВКИ.
Группа перестановок (таблица 1.3, задание №4):
        / 1 2 3 4 5 6 \
        \ 2 6 3 5 1 4 /
Представление исходного текста: ASCII-код.

Каждый символ исходного текста переводится в 8-битный ASCII-код,
полученная битовая последовательность разбивается на блоки по 6 бит,
внутри каждого блока биты переставляются по группе перестановок:
бит с позиции i переходит на позицию perm[i].
Последний неполный блок дополняется нулями (длина запоминается).
"""

# перестановка: бит на позиции i переходит на позицию PERM[i]
PERM = [2, 6, 3, 5, 1, 4]          # задание №4 таблицы 1.3
L = len(PERM)                       # длина блока = 6 бит


def text_to_bits(text):
    """Исходный текст -> последовательность бит (8-битные ASCII-коды)."""
    bits = []
    for ch in text:
        code = ord(ch)
        if code > 127:
            raise ValueError(f"Символ '{ch}' не входит в ASCII (код {code})")
        bits += [(code >> k) & 1 for k in range(7, -1, -1)]
    return bits


def bits_to_text(bits):
    """Последовательность бит -> текст (по 8 бит на символ)."""
    return "".join(
        chr(int("".join(map(str, bits[i:i + 8])), 2))
        for i in range(0, len(bits), 8)
    )


def permute(bits, perm):
    """Один 6-битный блок: бит с позиции i переходит на позицию perm[i]."""
    out = [0] * len(bits)
    for i, p in enumerate(perm):
        out[p - 1] = bits[i]
    return out


def encrypt(text, perm=PERM):
    """Шифрование: текст -> биты -> блоки по 6 -> перестановка -> биты."""
    bits = text_to_bits(text)
    n_bits = len(bits)                       # реальная длина до дополнения
    while len(bits) % L:                     # дополнение нулями
        bits.append(0)
    cipher = []
    for i in range(0, len(bits), L):
        cipher += permute(bits[i:i + L], perm)
    return cipher, n_bits


def inverse(perm):
    """Обратная перестановка."""
    inv = [0] * len(perm)
    for i, p in enumerate(perm):
        inv[p - 1] = i + 1
    return inv


def decrypt(cipher_bits, n_bits, perm=PERM):
    """Дешифрование: применяется обратная перестановка."""
    inv = inverse(perm)
    bits = []
    for i in range(0, len(cipher_bits), L):
        bits += permute(cipher_bits[i:i + L], inv)
    bits = bits[:n_bits]                     # отбросить дополнение
    return bits_to_text(bits)


def show(bits, group=6):
    """Печать битовой строки блоками по group бит."""
    return " ".join("".join(map(str, bits[i:i + group]))
                    for i in range(0, len(bits), group))


def main():
    text = input("Введите исходный текст (ASCII): ")
    print(f"\nПерестановка: (1 2 3 4 5 6) -> {tuple(PERM)}")

    ascii_bits = text_to_bits(text)
    print("\nASCII-коды символов:")
    for ch in text:
        print(f"  '{ch}' = {ord(ch):3d} = {ord(ch):08b}")

    cipher_bits, n_bits = encrypt(text)
    print("\nДвоичное представление исходного текста:")
    print(" ", show(ascii_bits))
    print("Криптограмма (биты, блоки по 6):")
    print(" ", show(cipher_bits))
    print("Криптограмма (символы):")
    print(" ", bits_to_text(cipher_bits))

    restored = decrypt(cipher_bits, n_bits)
    print("\nДешифрованный текст:")
    print(" ", restored)
    print("\nСовпадение с исходным:", restored == text)


if __name__ == "__main__":
    main()
