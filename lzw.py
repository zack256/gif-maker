import string

def simple_lzw_encode(s, starting_dictionary):

    dictionary = starting_dictionary.copy()
    encoding = []
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


def simple_lzw_decode():
    pass

# https://marknelson.us/posts/2011/11/08/lzw-revisited
print(simple_lzw_encode(
    "ABBABBBABBA",
    {"A" : 0, "B" : 1}
))
# https://en.wikipedia.org/wiki/Lempel-Ziv-Welch#Example
print(simple_lzw_encode(
    "TOBEORNOTTOBEORTOBEORNOT",
    {ch : i for i, ch in enumerate(string.ascii_uppercase)}
))
# https://stackoverflow.com/q/63493612
print(simple_lzw_encode(
    "ababcbababaaaaaaa",
    {"a" : 0, "b" : 1, "c" : 2}
))