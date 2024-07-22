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

def binary_lzw_encode(s, starting_dictionary, starting_width=None):

    minimum_starting_width = binary_utils.min_binary_width(len(starting_dictionary) - 1)
    if starting_width is None:
        starting_width = minimum_starting_width
    elif starting_width < minimum_starting_width:
        raise Exception("If given, [starting_width] must be able to represent every element in [starting_dictionary]!")
    
    dictionary = starting_dictionary.copy()
    encoding = []
    next_code = len(dictionary)
    current_width = starting_width

    print(dictionary)

    z = 0
    n = len(s)
    while z < n:
        z2 = z
        while z2 < n:
            if s[z : z2 + 1] in dictionary:
                z2 += 1
                if z2 == n:
                    encoding.append(binary_utils.int_to_binary_string_padded(dictionary[s[z : z2]], current_width))
            else:
                encoding.append(binary_utils.int_to_binary_string_padded(dictionary[s[z : z2]], current_width))
                if binary_utils.min_binary_width(next_code) != current_width:
                    current_width += 1
                dictionary[s[z : z2 + 1]] = next_code
                next_code += 1
                break
        z = z2
        
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
            if z:
                dictionary[next_code] = conjecture + dictionary[code][0]
                next_code += 1
        else:
            dictionary[next_code] = conjecture + conjecture[0]
            next_code += 1
        conjecture = dictionary[code]
        decoding += dictionary[code]
        z += 1

    return decoding

def binary_lzw_decode(encoding, starting_dictionary, starting_width=None):

    minimum_starting_width = binary_utils.min_binary_width(len(starting_dictionary) - 1)
    if starting_width is None:
        starting_width = minimum_starting_width
    elif starting_width < minimum_starting_width:
        raise Exception("If given, [starting_width] must be able to represent every element in [starting_dictionary]!")

    decoding = ""
    dictionary = starting_dictionary.copy()
    next_code = len(dictionary)
    current_width = starting_width

    z = 0
    conjecture = None
    while z < len(encoding):
        code = int(encoding[z : z + current_width], 2)
        if code in dictionary:
            if z:
                dictionary[next_code] = conjecture + dictionary[code][0]
                next_code += 1
        else:
            dictionary[next_code] = conjecture + conjecture[0]
            next_code += 1
        conjecture = dictionary[code]
        decoding += dictionary[code]
        
        z += current_width

        if binary_utils.min_binary_width(next_code) != current_width:
            current_width += 1

    return decoding

def test(s, starting_dictionary):
    encoded = simple_lzw_encode(s, starting_dictionary)
    print("Encoded:", encoded)
    decoded = simple_lzw_decode(encoded, { v : k for k, v in starting_dictionary.items() })
    print("Decoded:", decoded)
    if s == decoded:
        print("Match!")
    else:
        print("No match!")

def test_binary(s, starting_dictionary):
    encoded = binary_lzw_encode(s, starting_dictionary)
    print("Encoded:", encoded)
    decoded = binary_lzw_decode(encoded, { v : k for k, v in starting_dictionary.items() })
    print("Decoded:", decoded)
    if s == decoded:
        print("Match!")
    else:
        print("No match!")

# https://marknelson.us/posts/2011/11/08/lzw-revisited
# test(
#     "ABBABBBABBA",
#     {"A" : 0, "B" : 1}
# )
# https://en.wikipedia.org/wiki/Lempel-Ziv-Welch#Example
# test(
#     "TOBEORNOTTOBEORTOBEORNOT",
#     {ch : i for i, ch in enumerate(string.ascii_uppercase)}
# )
# https://stackoverflow.com/q/63493612
# test(
#     "ababcbababaaaaaaa",
#     {"a" : 0, "b" : 1, "c" : 2}
# )

test_binary(
    "ABBABBBABBA",
    {"A" : 0, "B" : 1}
)
test_binary(
    "TOBEORNOTTOBEORTOBEORNOT",
    {ch : i for i, ch in enumerate(string.ascii_uppercase)}
)
test_binary(
    "ababcbababaaaaaaa",
    {"a" : 0, "b" : 1, "c" : 2}
)