def opdracht2():
    list = [0,1,2,3]
    list[0] = 10
    print(list) # [10,1,2,3] 10 zal 0 vervangen

    # tuple = (0,1,2,3)
    # tuple[0] = 10
    # print(tuple) # TypeError: 'tuple' object does not support item assignment

    pass


def opdracht3():
    scores = [10,5,8,9,4,9,3,5,0,3,3,4]

    max_score = max(scores)
    min_score = min(scores)
    print(f"Max score is {max_score}")
    print(f"Min score is {min_score}")

    sorted_scores = sorted(scores)
    print(f"Twee groteste scores: ", sorted_scores[-2:])
    print(f"Twee kleinste scores: ", sorted_scores[:2])

    input_scores = input("Voer een lijst van gehele getallen in, gescheiden door spaties: ") 
    number_list = list(map(int, input_scores.split()))
    print("Totaal aantal items in de lijst:", len(number_list))

    if number_list:
        print("Laatste item in de lijst:", number_list[-1])

    print("Lijst in omgekeerde volgorde:", number_list[::-1])

    if 5 in number_list:
        print("Ja, de lijst bevat een 5.")
    else:
        print("Nee, de lijst bevat geen 5.")

    count_of_five = number_list.count(5)
    print("Aantal keren dat 5 voorkomt in de lijst:", count_of_five)

    if len(number_list) > 1:
        del number_list[0]  # Verwijder het eerste item
        del number_list[-1]  # Verwijder het laatste item
        number_list.sort()   # Sorteer de overgebleven items
        print("Lijst na verwijderen van eerste en laatste item en sorteren:", number_list)
    else:
        print("Niet genoeg items om het eerste en laatste item te verwijderen.")

    count_less_than_five = sum(1 for x in number_list if x < 5)
    print("Aantal gehele getallen kleiner dan 5:", count_less_than_five)

    pass

def opdracht4():
    import random

    random_numbers = [random.randint(1, 100) for _ in range(20)]

    print("Lijst van willekeurige getallen:", random_numbers)

    average = sum(random_numbers) / len(random_numbers)
    print("Gemiddelde van de elementen in de lijst:", average)

    max_value = max(random_numbers)
    min_value = min(random_numbers)
    print("Grootste waarde in de lijst:", max_value)
    print("Kleinste waarde in de lijst:", min_value)

    sorted_numbers = sorted(random_numbers)
    second_largest = sorted_numbers[-2]
    second_smallest = sorted_numbers[1]
    print("Op één na grootste waarde:", second_largest)
    print("Op één na kleinste waarde:", second_smallest)

    even_numbers = [number for number in random_numbers if number % 2 == 0]
    print("Aantal even getallen in de lijst:", len(even_numbers))

    pass

def opdracht5():
    my_list = [8, 9, 10]

    my_list[1] = 17
    print("Na het aanpassen van het tweede item:", my_list)

    my_list.extend([4, 5, 6])
    print("Na het toevoegen van 4, 5 en 6:", my_list)

    del my_list[0]
    print("Na het verwijderen van het eerste item:", my_list)

    my_list.sort()
    print("Na het sorteren van de lijst:", my_list)

    my_list = my_list * 2
    print("Na het verdubbelen van de lijst:", my_list)

    my_list.insert(3, 25)
    print("Na het toevoegen van 25 op index 3:", my_list)

    print("Uiteindelijke lijst:", my_list)

    pass

def opdracht6():

    list_a = []
    for  i in range(50):
        list_a.append(i)
    print("Lijst van gehele getallen van 0 tot en met 49:", list_a)

    list_b = []
    for i in range(1, 51):
        list_b.append(i ** 2)
    print("Lijst van gehele getallen van 1 tot en met 51:", list_b)

    list_c = []
    for i in range(1, 27):  # Van 1 tot 26
        list_c.append(chr(96 + i) * i)  # chr(97) = 'a', chr(98) = 'b', etc.
        list_c.append('z' * 26)  # Voeg 26 kopieën van 'z' toe
    print("Lijst met letters:", list_c)

    pass

def opdracht7():

    L = [3, 1, 4]
    M = [1, 5, 9]

    if len(L) != len(M):
        print("De lijsten moeten dezelfde lengte hebben.")
    else:
        N = [L[i] + M[i] for i in range(len(L))]
        print("De nieuwe lijst N is:", N)

    pass

def main():
    opdracht2()
    opdracht3()
    opdracht4()
    opdracht5()
    opdracht6()
    opdracht7()

if __name__ == '__main__':
    main()