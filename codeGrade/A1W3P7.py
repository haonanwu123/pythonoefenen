def turth_table():
    states = [(True,True), (True,False), (False,True),(False,False)]

    print("AND")
    for a,b in states:
        resalut = a and b
        print(f"{a} + {b} = {resalut}")

    print("OR")
    for a,b in states:
        resalut = a or b
        print(f"{a} + {b} = {resalut}")

turth_table()