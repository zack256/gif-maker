import os
import sys

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

def read_header(fi):
    signature = fi.read(3)
    version = fi.read(3)

def read_logical_screen_descriptor(fi):
    logical_screen_width = int.from_bytes(fi.read(2), "little")
    logical_screen_height = int.from_bytes(fi.read(2), "little")

    packed_fields = bytes_to_bit_list(fi.read(1))

    background_color_index = int.from_bytes(fi.read(1), "little")
    pixel_aspect_ratio = int.from_bytes(fi.read(1), "little")

def disect_gif_file (file_path):

    with open(file_path, "rb") as fi:
        read_header(fi)
        read_logical_screen_descriptor(fi)        

def main (*args):
    if args:
        local_path = args[0]
    else:
        local_path = "uncompressed_quilt.gif"
    abs_path = os.path.join(os.getcwd(), "data", local_path)
    return disect_gif_file(abs_path)

if __name__ == "__main__":
    main(*sys.argv[1:])