def convert_time(data, input_unit):
    if input_unit == "seconds":
        return data 
    if input_unit == "miliseconds":
        return data * 1000
    if input_unit == "microseconds":
        return data * 1000000
    else: 
        raise Exception("Unknown unit used.")

def convert_signal(data, unit, sensitivity, offset): 
    if unit == "V": 
        return data
    if unit == "mV":
        return data * 1000
    if unit == "Pa": 
        return pow(10,3) * ((data * sensitivity) + offset)
    else: 
        raise Exception("Unknown unit used.")
