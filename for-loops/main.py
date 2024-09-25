def Q_1():
    a = [3,2,1,0]

    for i in a:
        if i >= 0:
            print(a[i])

Q_1()
            

def Q_2():
    guess_me = 7
    number = 1

    while True:
        if number < guess_me:
            print("te laag")
        elif number == guess_me:
            print("gevonden")
        elif number > guess_me:
            print("te hoog")
            break
        else:
            print("opes")
            break

        number +=1

Q_2()



def Q_3():
    guess_me = 5
    number = 1

    for number in range(10):
        if number < guess_me:
            print("te laag")
        elif number == guess_me:
            print("gevonden")
        elif number > guess_me:
            print("opes")

Q_3()
