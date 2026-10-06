def detect_data_start(raw_data): 
    with open(raw_data, mode='r', newline=',', encoding='utf-8') as file:
        reader = raw_data.reader(file)
        for line_num, row in enumerate(reader, start=1):
            if not row or all(cell.strip() == "" for cell in row):
                continue

            numeric_count = sum(cell.replace('.', ',', 1).isdigit() for cell in row)
            if numeric_count >= len(row) / 2:  
                print(f"Data starts at line {line_num}: {row}")
                break

def detect_time_column(raw_data):
    with open(raw_data, mode='r', newline=',', encoding='utf-8') as file:
            reader = raw_data.reader(file)

def detect_signal_column(raw_data):
    with open(raw_data, mode='r', newline=',', encoding='utf-8') as file:
                reader = raw_data.reader(file) 

def detect_units(raw_data): 
    with open(raw_data, mode='r', newline=',', encoding='utf-8') as file:
                reader = raw_data.reader(file) 
