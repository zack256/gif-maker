import string

import binary_utils

# Starting dictionaries must be non-empty!

def simple_lzw_encode(s, starting_dictionary):

    encoding = []
    dictionary = starting_dictionary.copy()
    next_code = len(dictionary)

    z = 0
    n = len(s)
    while z < n:
        z2 = z
        while z2 < n:
            if s[z : z2 + 1] in dictionary:
                z2 += 1
                if z2 == n:
                    encoding.append(dictionary[s[z : z2]])
            else:
                encoding.append(dictionary[s[z : z2]])
                dictionary[s[z : z2 + 1]] = next_code
                next_code += 1
                break
        z = z2
        
    return encoding

def binary_lzw_encode(s, starting_dictionary, starting_width=None, clear_code=None):

    if clear_code is not None and clear_code not in starting_dictionary:
        raise Exception("[clear_code] must be in [starting_dictionary]")

    minimum_starting_width = binary_utils.min_binary_width(len(starting_dictionary) - 1)
    if starting_width is None:
        starting_width = minimum_starting_width
    elif starting_width < minimum_starting_width:
        raise Exception("If given, [starting_width] must be able to represent every element in [starting_dictionary]!")
    
    encoding = []
    dictionary = starting_dictionary.copy()
    next_code = len(dictionary)
    current_width = starting_width

    z = 0
    n = len(s)
    while z < n:
        z2 = z
        while z2 < n:
            if s[z : z2 + 1] in dictionary:
                if s[z : z2 + 1] == clear_code:
                    encoding.append(binary_utils.int_to_binary_string_padded(dictionary[clear_code], current_width))
                    z = z2 = z2 + 1
                    dictionary = starting_dictionary.copy()
                    next_code = len(dictionary)
                    current_width = starting_width
                    break
                z2 += 1
                if z2 == n:
                    encoding.append(binary_utils.int_to_binary_string_padded(dictionary[s[z : z2]], current_width))
            else:
                encoding.append(binary_utils.int_to_binary_string_padded(dictionary[s[z : z2]], current_width))
                if binary_utils.min_binary_width(next_code) > current_width:
                    current_width += 1
                dictionary[s[z : z2 + 1]] = next_code
                next_code += 1
                break
        z = z2
        
    # print(encoding)
    # return encoding
    return "".join(encoding)

def simple_lzw_decode(encoding, starting_dictionary):
    
    decoding = ""
    dictionary = starting_dictionary.copy()
    next_code = len(dictionary)

    z = 0
    conjecture = None
    while z < len(encoding):
        code = encoding[z]
        if code in dictionary:
            if conjecture is not None:
                dictionary[next_code] = conjecture + dictionary[code][0]
                next_code += 1
        else:
            dictionary[next_code] = conjecture + conjecture[0]
            next_code += 1
        conjecture = dictionary[code]
        decoding += dictionary[code]
        z += 1

    return decoding

def binary_lzw_decode(encoding, starting_dictionary, starting_width=None, clear_code=None, emit_clear_code=False):

    if clear_code is not None and clear_code not in starting_dictionary:
        raise Exception("[clear_code] must be in [starting_dictionary]")

    minimum_starting_width = binary_utils.min_binary_width(len(starting_dictionary) - 1)
    if starting_width is None:
        starting_width = minimum_starting_width
    elif starting_width < minimum_starting_width:
        raise Exception("If given, [starting_width] must be able to represent every element in [starting_dictionary]!")

    decoding = ""
    dictionary = starting_dictionary.copy()
    next_code = len(dictionary)
    current_width = starting_width
    
    conjecture = None

    z = 0
    while z < len(encoding):
        code = int(encoding[z : z + current_width], 2)

        if code == clear_code:
            if emit_clear_code:
                decoding += dictionary[code]
            z += current_width
            dictionary = starting_dictionary.copy()
            next_code = len(dictionary)
            current_width = starting_width
            conjecture = None
            continue

        if code in dictionary:
            if conjecture is not None:
                dictionary[next_code] = conjecture + dictionary[code][0]
                next_code += 1
        else:
            dictionary[next_code] = conjecture + conjecture[0]
            next_code += 1
        conjecture = dictionary[code]
        decoding += dictionary[code]
        
        z += current_width

        if binary_utils.min_binary_width(next_code) > current_width:
            current_width += 1

    return decoding

def construct_dictionary_from_alphabet(alphabet, prepend_hash=False):
    if prepend_hash:
        alphabet = "#" + alphabet
    return {ch : i for i, ch in enumerate(alphabet)}

def test_simple(s, starting_dictionary):
    encoded = simple_lzw_encode(s, starting_dictionary)
    print("Encoded:", encoded)
    decoded = simple_lzw_decode(encoded, { v : k for k, v in starting_dictionary.items() })
    print("Decoded:", decoded)
    if s == decoded:
        print("Match!")
    else:
        print("No match!")

def test_binary(s, starting_dictionary):
    print(f"String:     {s}")
    encoded = binary_lzw_encode(s, starting_dictionary, clear_code="#")
    print("Encoded:", encoded)
    decode_dictionary = { v : k for k, v in starting_dictionary.items() }
    decoded = binary_lzw_decode(encoded, decode_dictionary, clear_code=0, emit_clear_code=True)
    print(f"Decoded:    {decoded}")
    if s == decoded:
        print("Match!")
    else:
        print("No match!")

if __name__ == "__main__":

    # https://marknelson.us/posts/2011/11/08/lzw-revisited
    test_simple(
        "ABBABBBABBA",
        construct_dictionary_from_alphabet("AB")
    )
    # https://en.wikipedia.org/wiki/Lempel-Ziv-Welch#Example
    test_simple(
        "TOBEORNOTTOBEORTOBEORNOT",
        construct_dictionary_from_alphabet(string.ascii_uppercase)
    )
    # https://stackoverflow.com/q/63493612
    test_simple(
        "ababcbababaaaaaaa",
        construct_dictionary_from_alphabet("abc")
    )

    test_binary(
        "ABBABBB#ABBA",
        construct_dictionary_from_alphabet("AB", True)
    )
    test_binary(
        "TOBEORNOTTOBEORTOBE#ORNOT",
        construct_dictionary_from_alphabet(string.ascii_uppercase, True)
    )
    test_binary(
        "ababcbababa#aaaaaa",
        construct_dictionary_from_alphabet("abc", True)
    )
