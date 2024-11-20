import sys
import os


def tail_entire_file_to_list(filename):
    """Option 1: Load entire file into memory as a list and get the last 10 lines."""
    try:
        with open(filename, "r") as file:
            lines = []
            while True:
                line = file.readline()
                if not line:
                    break
                lines.append(line)
        return lines[-10:]
    except Exception as e:
        return f"Error reading file: {e}"


def tail_read_twice(filename):
    """Option 2: Read file twice, first to count lines, then to fetch the last 10 lines."""
    try:
        # First pass: count the total number of lines
        total_lines = 0
        with open(filename, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                total_lines += 1

        # Second pass: read the last 10 lines
        start_line = max(0, total_lines - 10)
        last_ten_lines = []
        with open(filename, "r") as file:
            for current_line in range(total_lines):
                line = file.readline()
                if current_line >= start_line:
                    last_ten_lines.append(line)
        return last_ten_lines
    except Exception as e:
        return f"Error reading file: {e}"


def tail_optimized(filename):
    """Option 3: Use a fixed-size buffer to store only the last 10 lines."""
    try:
        buffer = []
        with open(filename, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                buffer.append(line)
                if len(buffer) > 10:
                    buffer.pop(0)
        return buffer
    except Exception as e:
        return f"Error reading file: {e}"


def main():
    # Validate input
    if len(sys.argv) != 2:
        print("Usage: python3 tail.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(filename):
        print(f'Error reading file: "{filename}" does not exist')
        sys.exit()

    # Output results
    print("\n--- Reading the last 10 lines of the file ---")
    for option, func in enumerate(
        [tail_entire_file_to_list, tail_read_twice, tail_optimized], start=1
    ):
        print(f"\nOption {option} Output:")
        last_ten_lines = func(filename)
        if isinstance(last_ten_lines, list):
            print("".join(last_ten_lines))
        else:
            print(last_ten_lines)


if __name__ == "__main__":
    main()
