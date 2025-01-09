def get_num_of_vowels(inp: str) -> int:
    vowels = "aeiouAEIOU"
    vowel_count = sum(1 for char in inp if char in vowels)
    return vowel_count


def sort_basedon_vowels():
    cases = ["code", "programming", "description", "fly", "free"]
    sorted_cases = sorted(cases, key=get_num_of_vowels)
    print(sorted_cases)


if __name__ == "__main__":
    sort_basedon_vowels()
