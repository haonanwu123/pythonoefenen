def next_verse(verse_number: int) -> str:
    gifts = [
        "A partridge in a pear tree",
        "Two turtledoves",
        "Three French hens",
        "Four calling birds",
        "fivegoldrings(Five golden rings)",
        "Six geese a-laying",
        "Seven swans a-swimming",
        "Eight maids a-milking",
        "Nine ladies dancing",
        "Ten lords a-leaping",
        "Eleven pipers piping",
        "Twelve drummers drumming"
    ]

    ordinal = ["1st", "2nd", "3rd"] + [f"{i}th" for i in range(4, 13)]
    
    verse = f"On the {ordinal[verse_number - 1]} day of Christmas, my true love sent to me"
    
    if verse_number == 1:
        gift1 = " " + gifts[0]
        verse += gift1
    else:
        for i in range(verse_number - 1, 0, -1):
            if i == verse_number - 1:
                verse += " " + gifts[i]
            else:
                verse += ", " + gifts[i]
        verse += " And " + gifts[0]
    
    return verse


def main():
    for day in range(1, 13):
        print(next_verse(day))

if __name__ == "__main__":
    main()
