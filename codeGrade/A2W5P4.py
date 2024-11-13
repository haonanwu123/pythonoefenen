def is_integer(unchecked: str) -> bool:
    unchecked = unchecked.strip()
    
    if len(unchecked) == 0:
        return False
    
    if unchecked[0] in ['+', '-']:
        sign = unchecked[0]
        unchecked = unchecked[1:]
    
    return unchecked.isdigit()

def remove_non_integer(unchecked: str) -> int:
    unchecked = unchecked.strip()

    sign = ''
    
    for char in unchecked:
        if char == '+' or char == '-':
            sign = char
            break
    
    cleaned = ''.join(char for char in unchecked if char.isdigit())
    
    if cleaned == '':
        return 0
    
    return int(sign + cleaned) if sign else int(cleaned)

def main():
    unchecked_str = input("Enter a string: ")

    if is_integer(unchecked_str):
        print("Valid integer")
    else:
        print("Invalid integer")
        cleaned_integer = remove_non_integer(unchecked_str)
        print(f"Remaining integer: {cleaned_integer}") 

if __name__ == "__main__":
    main()