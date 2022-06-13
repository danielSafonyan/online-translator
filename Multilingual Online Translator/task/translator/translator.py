import string


def increment_string(my_str):
    digit_idx = None

    for idx, letter in enumerate(my_str):
        if letter in string.digits:
            digit_idx = idx
            break

    digit_portion = my_str[digit_idx:]

    if int(digit_portion) == 0:
        return my_str[:-1] + '1'

testing_string = 'hello'
print(testing_string[:-1])