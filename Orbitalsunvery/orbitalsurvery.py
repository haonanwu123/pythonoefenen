def decimal_to_binary(number: int, cells_cnt: int) -> list:
    """
    Converts the number to the binary representation in a list
    :param number: The number to convert
    :param cells_cnt: The number of cells in the matrix
    :return: List with zero's and one's
    """
    binary_str = f"{number:b}"
    zero_pad_cnt = cells_cnt - len(binary_str)
    zero_pad = "".join("0" for x in range(0, zero_pad_cnt))
    binary_str = zero_pad + binary_str
    rvalue = [x for x in binary_str]
    return rvalue


def convert_to_columns(the_list: list, rows: int, cols: int) -> list:
    """
    Converts the list with zero's and one's into multiple lists. Each list
    represents a seperate column
    :param the_list: The list with zero's and one's.
    :param rows: Number of rows
    :param cols: Number of columns
    :return: List with list.
    """
    list_columns = []
    for offset in range(0, cols):
        list_column = []
        lookup_index = []
        for row in range(0, rows):
            lookup_index.append((row * cols) + offset)

        for idx in lookup_index:
            list_column.append(the_list[idx])

        list_columns.append(list_column)

    return list_columns


def find_highest_consecutive(columns: list, value: str) -> list:
    """
    Find the highest number of consecutive values of 'value' in the columns
    :param columns: The columns to search
    :param value: The value to find
    :return: The highest count of consecutive instances of 'value' for each column
    """

    highest_counts = []
    for column in columns:
        highest_cnt = 0
        for idx in range(-1, 0 - len(column) - 1, -1):
            v_ = column[idx]
            if v_ == value:
                highest_cnt += 1
            else:
                break
        highest_counts.append(highest_cnt)

    return highest_counts


def analyse_scan(rows: int, cols: int, datastream: int) -> int:
    """
    Analyse the data-scan from the orbitor
    :param rows: Number of rows
    :param cols: Number of columns
    :param datastream: The datastream
    :return: The highest point of the land.
    """
    binary_str = decimal_to_binary(datastream, rows * cols)
    columns = convert_to_columns(binary_str, rows, cols)
    highest_count = max(find_highest_consecutive(columns, '1'))
    return highest_count


def main():
    with open("./Orbitalsunvery/orbitalsuverydata.txt") as datafile:
        for datafileline in datafile.readlines():
            r, c, a = map(int, datafileline.split(","))
            highest = analyse_scan(r, c, a)
            print(f"{highest}")


if __name__ == "__main__":
    main()
