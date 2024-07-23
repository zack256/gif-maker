def min_binary_width(n):
    return len(bin(n)) - 2

def int_to_binary_string_padded(n, width):
    non_padded = bin(n)[2:]
    return "0" * (width - len(non_padded)) + non_padded

def bytes_to_bit_list(byts):
    bits = []
    for byte in byts:
        bin_string = bin(byte)[2:]
        bin_string = "0" * (8 - len(bin_string)) + bin_string
        bits += list(bin_string)
    return bits

def bit_list_to_bytes(bit_list):
    byts = []
    if len(bit_list) > 8 and len(bit_list) % 8:
        raise Exception("If multiple bits, bit list must be divisible by 8")
    for i in range(0, len(bit_list), 8):
        byts.append(int("".join(map(str, bit_list[i : i + 8])), 2))
    return bytes(byts)
