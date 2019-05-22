# Pascalle Veltman: 11025646
# converts CSV file to json

import csv, json
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# read csv file and save as dataframe
df = pd.read_csv(r'/Users/pascalleveltman/Documents/GitHub/dataprocessing/Homework/Week_6/HuwelijkenWeek6.csv')
df = df.loc[[0,2,3,4]]
df = df[['Soort', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']]
df = df.set_index('Soort')

# define json file to write to
json_file = df.to_json(r'/Users/pascalleveltman/Documents/GitHub/dataprocessing/Homework/Week_6/Huwelijken_json.json', orient='columns')
