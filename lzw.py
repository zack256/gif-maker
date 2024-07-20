import string

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

def test(s, starting_dictionary):
    encoded = simple_lzw_encode(s, starting_dictionary)
    print("Encoded:", encoded)
    decoded = simple_lzw_decode(encoded, { v : k for k, v in starting_dictionary.items() })
    print("Decoded:", decoded)
    if s == decoded:
        print("Match!")
    else:
        print("No match!")

# https://marknelson.us/posts/2011/11/08/lzw-revisited
test(
    "ABBABBBABBA",
    {"A" : 0, "B" : 1}
)
# https://en.wikipedia.org/wiki/Lempel-Ziv-Welch#Example
test(
    "TOBEORNOTTOBEORTOBEORNOT",
    {ch : i for i, ch in enumerate(string.ascii_uppercase)}
)
# https://stackoverflow.com/q/63493612
test(
    "ababcbababaaaaaaa",
    {"a" : 0, "b" : 1, "c" : 2}
)