def Q_One():
    for Andrej in [True, False]:
        for Babak in [True, False]:
            for Cigdem in [True, False]:
                if (Andrej == (not Babak) and
                    Babak == (not Cigdem) and
                    Cigdem == (not Andrej and not Babak)):
                    return (Andrej, Babak, Cigdem)
    return None

def main():
    result = Q_One()
    if result:
        Andrej, Babak, Cigdem = result
        truth_status = lambda x: 'is not a liar' if x else 'is a liar'
        print(f"Andrej {truth_status(Andrej)}")
        print(f"Babak {truth_status(Babak)}")
        print(f"Cigdem {truth_status(Cigdem)}")
    else:
        print("No consistent solution found.")

main()
