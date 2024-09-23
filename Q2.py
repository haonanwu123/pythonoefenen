def Q_Two():
    for Andrej in [True, False]:
        for Babak in [True, False]:
            for Cigdem in [True, False]:
                andrej_statement = not (Andrej and Babak) or not Cigdem
                Babak_statement = Andrej
                Cigdem_statement = Cigdem

                if (Andrej == andrej_statement and
                    Babak == Babak_statement and
                    Cigdem == Cigdem_statement):
                    return (Andrej, Babak, Cigdem)
    return None

def main():
    result = Q_Two()
    if result:
        Andrej, Babak, Cigdem = result
        truth_status = lambda x: 'is not a liar' if x else 'is a liar'
        print(f"Andrej {truth_status(Andrej)}")
        print(f"Babak {truth_status(Babak)}")
        print(f"Cigdem {truth_status(Cigdem)}")
    else:
        print("No consistent solution found.")

main()