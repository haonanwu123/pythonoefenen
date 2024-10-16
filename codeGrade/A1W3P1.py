def word_reverse(user_input):
    new_string = ""
    for i in range(len(user_input)-1, -1, -1):
        new_string += user_input[i]
    return new_string

def clean_string(user_input):
    cleaned_string = ''.join(char.lower() for char in user_input if char.isalpha())
    return cleaned_string

def is_palindromic_words():
    user_input = input("Enter a string: ").strip()
    
    cleaned_input = clean_string(user_input)
    
    reversed_string = word_reverse(cleaned_input)
    
    if reversed_string == cleaned_input:
        print(f'"{reversed_string}" is a palindrome')
    else:
        print(f'"{reversed_string}" is not a palindrome')

if __name__ == "__main__":
    is_palindromic_words()
