import csv
import numpy as np

def detect_data_start(csv_file):
    with open(csv_file, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for data_start, row in enumerate(reader):
            values = [cell.strip() for cell in row if cell.strip()]

            if not values:
                continue

            numeric_count = 0

            for value in values:
                try:
                    float(value)
                    numeric_count += 1
                except ValueError:
                    pass

            if numeric_count >= 2 and numeric_count >= len(values) / 2:
                return data_start

    return None

def detect_time_column(data):
    candidates = []

    for column in data.columns:
        values = data[column].dropna().to_numpy()

        if len(values) < 2:
            continue

        differences = np.diff(values)

        if np.all(differences > 0):
            candidates.append(column)

    if len(candidates) == 1:
        return candidates[0]

    return None


def detect_signal_columns(data, time_column):
    signal_columns = [
    column for column in data.columns
    if column != time_column
    ]

    return signal_columns
