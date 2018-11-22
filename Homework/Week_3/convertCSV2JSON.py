# Pascalle Veltman: 11025646
# converts CSV file to jason

import csv, json
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# define the input and output files
csv_file = "horeca.csv"
json_file = "horeca_json.json"

# read CSV file and store important data
with open(csv_file) as csv_data:
    csv_reader = csv.DictReader(csv_data)
    data = {}

    for row in csv_reader:
        data_row = {}

        # couple keys to values of each row
        for key, value in row.items():
            data_row[key] = value

        # define key for row
        row_key = row['Perioden']

        # change name of periods so that the program can read it
        if '1e' in row_key:
            row_key = row_key.replace(" 1e kwartaal", "-01-01")
        elif '2e' in row_key:
            row_key = row_key.replace(" 2e kwartaal", "-04-01")
        elif '3e' in row_key:
            row_key = row_key.replace(" 3e kwartaal", "-07-01")
        elif '4e' in row_key:
            row_key = row_key.replace(" 4e kwartaal", "-10-01")

        # remove symbols
        if '*' in row_key:
            row_key = row_key.replace("*", "")

        # add data and key to complete set
        data[row_key] = data_row

# write to json file
with open(json_file, "w") as json_data:
    json_data.write(json.dumps(data))
