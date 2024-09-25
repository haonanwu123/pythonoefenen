def solve_puzzle():
    for football_group in [True, False]:
        rugby_group = not football_group

        for Andrej in [True, False]:
            for Babak in [True, False]:
                for Cigdem in [True, False]:
                    andrej_statement = (Babak == rugby_group)
                    babak_statement = (Cigdem == football_group)
                    cigdem_statement = (Andrej == football_group and Babak == rugby_group)

                    is_andrej_truthful = (Andrej == football_group)
                    is_babak_truthful = (Babak == football_group)
                    is_cigdem_truthful = (Cigdem == football_group)

                    if (is_andrej_truthful == andrej_statement and
                        is_babak_truthful == babak_statement and
                        is_cigdem_truthful == cigdem_statement):
                        return {
                            'Andrej': 'plays football' if Andrej == football_group else 'plays rugby',
                            'Babak': 'plays football' if Babak == football_group else 'plays rugby',
                            'Cigdem': 'plays football' if Cigdem == football_group else 'plays rugby'
                        }

    return None

def main():
    result = solve_puzzle()
    if result:
        print("Solution found:")
        for person, role in result.items():
            print(f"{person} {role}")
    else:
        print("No consistent solution found.")

main()
