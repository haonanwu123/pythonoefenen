temperatures = (
    ('1995', '3', ['47.3', '40.0', '38.3', '36.3', '37.4', '40.3', '41.1', '40.5', '41.6', '43.2', '46.2', '45.8', '44.9', 
                    '39.4', '40.5', '42.0', '46.5', '46.2', '43.3', '41.7', '40.7', '39.6', '44.2', '47.8', '45.9', 
                    '47.3', '39.8', '35.2', '38.5', '40.5', '47.0']),
    ('2010', '3', ['39.2', '36.7', '35.5', '35.2', '35.8', '33.8', '30.7', '33.2', '32.3', '33.3', '37.3', '39.9', 
                    '40.8', '42.9', '42.7', '42.6', '44.8', '50.3', '52.2', '55.2', '47.2', '45.0', '48.6', '55.0', 
                    '57.4', '50.9', '48.6', '46.2', '49.6', '50.1', '43.6']),
    ('2020', '3', ['43.2', '41.1', '40.0', '43.6', '42.6', '44.0', '44.0', '47.9', '46.6', '50.5', '51.5', '47.7', 
                    '44.7', '44.0', '48.9', '45.3', '46.6', '49.7', '47.2', '44.8', '41.8', '40.9', '41.0', '42.7', 
                    '43.4', '44.0', '46.4', '45.5', '40.7', '39.5', '40.6'])
)


def process_temperature_data(data):
    march_1995 = set(float(temp) for temp in data[0][2])
    march_2010 = set(float(temp) for temp in data[1][2])
    march_2020 = set(float(temp) for temp in data[2][2])

    common_1995_2010 = march_1995.intersection(march_2010)
    answer_1 = len(common_1995_2010)

    common_1995_2020 = march_1995.intersection(march_2020)
    answer_2 = len(common_1995_2020)

    max_temp_1995 = max(march_1995)
    max_temp_2010 = max(march_2010)
    max_temp_2020 = max(march_2020)

    highest_temp = max(max_temp_1995, max_temp_2010, max_temp_2020)
    if highest_temp == max_temp_1995:
        answer_3 = '1995'
    elif highest_temp == max_temp_2010:
        answer_3 = '2010'
    else:
        answer_3 = '2020'

    avg_temp_1995 = sum(march_1995) / len(march_1995)
    avg_temp_2010 = sum(march_2010) / len(march_2010)
    avg_temp_2020 = sum(march_2020) / len(march_2020)

    warmest_avg_temp = max(avg_temp_1995, avg_temp_2010, avg_temp_2020)

    if warmest_avg_temp == avg_temp_1995:
        answer_4 = '1995'
    elif warmest_avg_temp == avg_temp_2010:
        answer_4 = '2010'
    else:
        answer_4 = '2020'

    return answer_1, answer_2, answer_3, answer_4


def main():
    answers = process_temperature_data(temperatures)
    for index, answer in enumerate(answers, start=1):
        print(f"Answer_{index}: {answer}")

if __name__ == "__main__":
    main()