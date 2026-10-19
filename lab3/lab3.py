# -*- coding: utf-8 -*-
"""
Лабораторная работа № 3. Вариант 11.
Модифицированная сеть Фейстеля (4 ветви по 32 бита, блок 128 бит,
ключ 64 бита). Число раундов n = 28.
Образующая функция: УМНОЖЕНИЕ ПО МОДУЛЮ 2^N (N = 32):
    F_i = (X1(i-1) * V_i(K)) mod 2^32
Параметр сети:  V_i(K) = (K1 ROL i) XOR (K2 ROR i),
K1, K2 - левая и правая 32-битные половины ключа K.

Итерация шифрования:
    X1(i) = X2(i-1) XOR F_i
    X2(i) = X3(i-1)
    X3(i) = X4(i-1)
    X4(i) = X1(i-1)
"""

MASK32 = 0xFFFFFFFF
N_ROUNDS = 28          # число раундов по варианту


def rol(x, i, w=32):
    """Циклический сдвиг влево на i бит (w-разрядное слово)."""
    i %= w
    return ((x << i) | (x >> (w - i))) & MASK32


def ror(x, i, w=32):
    """Циклический сдвиг вправо на i бит."""
    i %= w
    return ((x >> i) | (x << (w - i))) & MASK32


def net_param(i, k1, k2):
    """V_i(K) = K1 ROL i  XOR  K2 ROR i."""
    return rol(k1, i) ^ ror(k2, i)


def round_f(x1, v):
    """Образующая функция варианта 11: умножение по модулю 2^32."""
    return (x1 * v) & MASK32


def encrypt_block(block, key):
    """Один 128-битный блок -> 128-битная криптограмма."""
    x1, x2, x3, x4 = block
    k1, k2 = (key >> 32) & MASK32, key & MASK32
    for i in range(1, N_ROUNDS + 1):
        f = round_f(x1, net_param(i, k1, k2))
        x1, x2, x3, x4 = x2 ^ f, x3, x4, x1
    return x1, x2, x3, x4


def decrypt_block(block, key):
    """Обратная итерация (та же сеть, инверсный порядок параметров)."""
    x1, x2, x3, x4 = block
    k1, k2 = (key >> 32) & MASK32, key & MASK32
    for i in range(N_ROUNDS, 0, -1):
        # X1(i-1)=X4(i); X2(i-1)=X1(i)^F_i; X3(i-1)=X2(i); X4(i-1)=X3(i)
        f = round_f(x4, net_param(i, k1, k2))
        x1, x2, x3, x4 = x4, x1 ^ f, x2, x3
    return x1, x2, x3, x4


def to_blocks(data):
    """bytes -> список 128-битных блоков (x1,x2,x3,x4)."""
    pad = (-len(data)) % 16
    data = data + b"\x00" * pad
    blocks = []
    for i in range(0, len(data), 16):
        blocks.append(tuple(
            int.from_bytes(data[i + 4 * j: i + 4 * j + 4], "big")
            for j in range(4)))
    return blocks, pad


def from_blocks(blocks, pad):
    data = b"".join(x.to_bytes(4, "big") for b in blocks for x in b)
    return data[:-pad] if pad else data


def main():
    text = input("Введите исходный текст: ")
    key = int(input("Введите 64-битный ключ (16 hex-цифр, напр. "
                    "0123456789ABCDEF): "), 16)
    print(f"\nРаундов: {N_ROUNDS}; образующая функция: "
          f"F = X1 * V_i mod 2^32; V_i = K1 ROL i XOR K2 ROR i")
    print(f"K1 = {key >> 32:08X}, K2 = {key & MASK32:08X}")

    data = text.encode("utf-8")
    blocks, pad = to_blocks(data)
    print(f"\nИсходный текст: {text!r}")
    print(f"Блоков по 128 бит: {len(blocks)} (дополнено {pad} байт)")
    for i, b in enumerate(blocks):
        print(f"  блок {i}: " + " ".join(f"{x:08X}" for x in b))

    enc = [encrypt_block(b, key) for b in blocks]
    print("\nКриптограмма:")
    for i, b in enumerate(enc):
        print(f"  блок {i}: " + " ".join(f"{x:08X}" for x in b))
    print("  hex:", from_blocks(enc, 0).hex().upper())

    dec = [decrypt_block(b, key) for b in enc]
    restored = from_blocks(dec, pad).decode("utf-8")
    print("\nДешифрованный текст:", restored)
    print("Совпадение с исходным:", restored == text)


if __name__ == "__main__":
    main()
