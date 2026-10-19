#This program file is primarily used for the "detect" button
#within the frontend. It allows for the user to not have
#to manually input what each column does. Instead, 
#it attempts to guess what each column and row is and
#user is able to confirm it. 

import csv
import numpy as np

def detect_data_start(csv_file):
    """ 
    Typically in the DAQ files there are a couple rows in the beginning
    that do not have any data, but instead have other information such as 
    unit type. If left alone, this information can cause errors for the 
    rest of the calculation. This function detects when two sequential rows
    have pure numerical values, then it saves the counter which will then be used 
    by "read_data" in loader.py. 
    """
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
    # TODO : Add a way for users to confirm this is the proper amount 
    # of rows skipped 
    # TODO: It may be useful to increase the amount of confirmation to 
    # 3-5 rows depending on how other DAQ systems format files 

def detect_time_column(data):
    """
    This is used when the user clicks the "detect" button in 
    the frontend of the program. It is able to detect which
    column is likely for time by testing if the values are
    the same distance away from another. EX: If a system is 
    checking for new data every 1 milisecond, then each time 
    column value should be 1 milisecond apart. 
    """
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
    # If a detection did not work properly
    # it made more sense to simply not do anything, 
    # then to do something that was wrong. 


def detect_signal_columns(data, time_column):
    """
    This is used alongside detect_time_column when a user
    hits the "detect" button. This program simply takes the 
    result of the time_column and assumes every other column 
    that is not for time is for signal channels. 
    """
    signal_columns = [
    column for column in data.columns
    if column != time_column
    ]

    return signal_columns

    # TODO: Add a detect_units function, this  
    # likely will only be able to be properly implemented
    # for QuickDAQ .csv files without looking at how
    # other systems display the units. 
