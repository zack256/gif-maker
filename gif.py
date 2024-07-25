import os
import sys

import binary_utils

def read_header(fi):
    signature = fi.read(3)
    version = fi.read(3)

def read_logical_screen_descriptor(fi):
    logical_screen_width = int.from_bytes(fi.read(2), "little")
    logical_screen_height = int.from_bytes(fi.read(2), "little")

    packed_fields = binary_utils.bytes_to_bit_list(fi.read(1))
    global_color_table_flag = packed_fields[0]
    color_resolution = int.from_bytes(binary_utils.bit_list_to_bytes(packed_fields[1:4]), "little")
    sort_flag = packed_fields[4]
    size_of_global_color_table = int.from_bytes(binary_utils.bit_list_to_bytes(packed_fields[5:]), "little")

    background_color_index = int.from_bytes(fi.read(1), "little")
    pixel_aspect_ratio = int.from_bytes(fi.read(1), "little")

    return size_of_global_color_table

def read_global_color_table(fi, size_of_global_color_table):
    number_of_rgb_colors = 2 ** (size_of_global_color_table + 1)
    global_color_table = []
    for i in range(number_of_rgb_colors):
        red = int.from_bytes(fi.read(1), "little")
        green = int.from_bytes(fi.read(1), "little")
        blue = int.from_bytes(fi.read(1), "little")
        global_color_table.append((red, green, blue))
    return global_color_table

def read_image_descriptor(fi):
    image_separator = fi.read(1)
    if image_separator != b',':
        raise Exception("GIF error: Image Separator must be 0x2C")
    image_left_position = int.from_bytes(fi.read(2), "little")
    image_top_position = int.from_bytes(fi.read(2), "little")
    image_width = int.from_bytes(fi.read(2), "little")
    image_height = int.from_bytes(fi.read(2), "little")

    packed_fields = binary_utils.bytes_to_bit_list(fi.read(1))
    local_color_table_flag = packed_fields[0]
    interlace_flag = packed_fields[1]
    sort_flag = packed_fields[2]
    # 2 bits ([3] and [4]) are reserved.
    size_of_local_color_table = int.from_bytes(binary_utils.bit_list_to_bytes(packed_fields[5:]), "little")

def read_table_based_image_data(fi, color_table):
    lzw_minimum_code_size = int.from_bytes(fi.read(1), "little")
    clear_code = 2 ** lzw_minimum_code_size
    end_of_information_code = clear_code + 1
    
    image_data = b''

    blocks_read = 0
    while True:
        block_size = int.from_bytes(fi.read(1), "little")
        if block_size == 0:
            break
        block = fi.read(block_size)
        image_data += block
        blocks_read += 1

def disect_gif_file (file_path):

    with open(file_path, "rb") as fi:
        read_header(fi)
        size_of_global_color_table = read_logical_screen_descriptor(fi)
        global_color_table = read_global_color_table(fi, size_of_global_color_table)
        read_image_descriptor(fi)   
        read_table_based_image_data(fi, global_color_table)

def main (*args):
    if args:
        local_path = args[0]
    else:
        local_path = "uncompressed_quilt.gif"
    abs_path = os.path.join(os.getcwd(), "data", local_path)
    return disect_gif_file(abs_path)

if __name__ == "__main__":
    main(*sys.argv[1:])