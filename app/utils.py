import string
import random

def randomize_bot_names(name, number_of_ints=3, number_of_chars=1, string_list=None ):
    if not string_list:
        string_list = [':', ':', ':', ':', ':', ':', ':', ':', ':', ':',
                       ':', ':', ':', ':', ':', ':', ':', ':', ':', ':',
                       ':', ':', ':', ':', ':', ':', ':', ':', ':', ':',
                       '(:)', '(: )']

    ran_int = ''.join(random.choices(string.digits, k=number_of_ints))
    ran_char = ''.join(random.choices(string.ascii_uppercase, k=number_of_chars))
    string_a, string_b = ''.join(random.choices(string_list, k=1)).split(':')

    return f'{name} {string_a}{ran_int}{ran_char}{string_b}'


def token_generator(length=30):
    LETTERS = string.ascii_letters
    NUMBERS = string.digits

    printable = f'{LETTERS}{NUMBERS}'
    printable = list(printable)
    random.shuffle(printable)

    token = random.choices(printable, k=length)
    token = ''.join(token)
    return token