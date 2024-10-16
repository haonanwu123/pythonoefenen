def sentence_reverse(user_input):
    new_sentence = ""

    for i in range(len(user_input)-1,-1,-1):
        new_sentence += user_input[i]
        
    return new_sentence


def clean_sentence(user_input):
    cleaned_sentence = ''.join(char.lower() for char in user_input if char.isalpha())

    return cleaned_sentence

def main():
    user_input = input("Sentence:")
    sentence = clean_sentence(user_input)
    sentence_reversed = sentence_reverse(sentence)

    if not user_input.isalpha() and not user_input.strip():
        print("Error: Input contains non-alphabet characters.")
    elif sentence == sentence_reversed:
        print(f'"{user_input}" is a palindrome')
    else:
        print(f'"{user_input}" is not a palindrome')

if __name__ == "__main__":
    main()