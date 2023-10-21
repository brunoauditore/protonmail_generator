from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import random
from faker import Faker


def generate_password(min_length, max_length, use_special_symbols=False, use_digits=False, custom_symbols=None):
    length = random.randint(min_length, max_length)
    if use_special_symbols and use_digits:
        possible_chars = ascii_uppercase + ascii_lowercase + digits + punctuation
    elif use_digits:
        possible_chars = ascii_uppercase + ascii_lowercase + digits
    elif use_special_symbols:
        possible_chars = ascii_uppercase + ascii_lowercase + punctuation
    else:
        possible_chars = ascii_uppercase + ascii_lowercase

    first_char = random.choice(ascii_lowercase)
    length -= 1

    random_string = ''
    for _ in range(length):
        random_string += random.choice(possible_chars)
    random_string = first_char + random_string

    if custom_symbols:
        random_list = list(random_string)
        last_index = 0
        for symbol in custom_symbols:
            current_index = random.randint(1, length-1)
            if current_index == last_index:
                current_index += 2
            elif current_index == last_index+1:
                current_index += 1
            elif current_index == last_index-1:
                current_index += 3

            random_list.insert(current_index, symbol)
            last_index = current_index
        random_string = ''.join(random_list)
    return random_string


def get_username():
    fake = Faker()
    adjectives = []
    nouns = []

    adjectives.extend([fake.word() for _ in range(90)])
    nouns.extend([fake.word()[::-1] for _ in range(90)])
    use_delimiter = False

    res = ''
    for _ in range(random.randint(2, 4)):
        delimiter = random.choice(('-', "", "_")) if use_delimiter else ""
        res += random.choice(adjectives) + delimiter + random.choice(nouns)

    res += "" if random.choice([True, False]) else generate_password(6, 10, use_digits=True)
    # if len(res) > 39:
    #     res = res[0:random.randint(22, 37)]
    # if len(res) <= 20:
    #     res += generate_password(5, 8, use_digits=True)
    if len(res) > 10:
        res = res[:10]
    return res.lower()


# for i in range(30):
#     result = get_username()
#     print(result)
#     print(len(result))
#     print()
