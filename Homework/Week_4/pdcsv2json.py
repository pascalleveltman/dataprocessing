# Pascalle Veltman: 11025646
# converts CSV file to jason

import csv, json
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# read csv file and save as dataframe
df = pd.read_csv(r'/Users/pascalleveltman/Documents/GitHub/dataprocessing/Homework/Week_4/Huwelijken.csv')
df = df[df["Perioden"] == 2017]
df = df[['Soort', 'Waarde']]
df= df.drop([67, 135, 203])
# df = df.set_index('Soort')
print(df)

# define json file to write to
json_file = df.to_json(r'/Users/pascalleveltman/Documents/GitHub/dataprocessing/Homework/Week_4/Huwelijken_json.json', orient='records')
