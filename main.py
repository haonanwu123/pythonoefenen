# def fib(n):
#     if n <= 1:
#         return n
#     return fib(n - 1) + fib(n - 2)

# print(fib(4))

# li = ['a', 'b', 'c']
# while li:
#     print(li.pop(), end=' ')


# data_list = [[]] * 3 # output [[], [], []]
# data_list[0].append(10)# output [[10], [10], [10]]
# data_list[1].append(20)# output [[10,20], [10,20], [10,20]]
# print(data_list)

# data_list = [[] for _ in range(3)]# output [[], [], []]
# data_list[0].append(10)# output [[10], [], []]
# data_list[1].append(20)# output [[10], [20], []]
# print(data_list)


# def func(n):
#     if n:
#         return n + func(n-1)
#     else:
#         return n

# print(func(3)) #output 3+(2+(1+(0)))

import random


def generate_password(length):
    if length < 4:
        raise ValueError(
            "Password length should be at least 4 to meet all requirements."
        )

    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digit = "0123456789"
    special_character = "!@#$%^&*()?|,.`~=+-_"

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digit),
        random.choice(special_character),
    ]

    all_characters = lowercase + uppercase + digit + special_character
    password += random.choices(all_characters, k=length - len(password))

    random.shuffle(password)

    return "".join(password)


while True:
    try:
        length = int(input("How long do you want your password to be? "))
        if length >= 4:
            break
        else:
            print("Password length must be at least 4 characters.")
    except ValueError:
        print("Please enter a valid number.")


password = generate_password(length)
print("Password: " + password)
