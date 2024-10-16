MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...',
    'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',
    'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-',
    'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--',
    'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ',': '--..--', '.': '.-.-.-',
    '?': '..--..'}

MORSE_TO_TEXT_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

def message_to_morse(message):
    morse_message = []
    for char in message.upper():
        if char in MORSE_CODE_DICT:
            morse_message.append(MORSE_CODE_DICT[char])
        elif char == " ":
            morse_message.append("  ")
        else:   
            print(f"Can't convert char [{char}]")
            return None
    return ' '.join(morse_message) + ' '


def morse_to_message(morse_code):
    message = []
    morse_words = morse_code.split("   ")

    for morse_word in morse_words:
        morse_chars = morse_word.strip().split(" ")
        
        for morse_char in morse_chars:
            if morse_char in MORSE_TO_TEXT_DICT:
                message.append(MORSE_TO_TEXT_DICT[morse_char])
            else:
                print(f"Can't convert Morse code [{morse_char}]")
                return None
        
        message.append(" ")
    return ''.join(message).strip().lower()


def translate_text(text):
    if all(char in ["-", ".", " "] for char in text):
        return morse_to_message(text)
    else:
        return message_to_morse(text)
    

def main():
    user_input = input("Enter a message: ")

    translated = translate_text(user_input)

    if translated is not None:
        print(translated)


if __name__ == "__main__":
    main()