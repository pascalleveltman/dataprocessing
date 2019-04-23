#!/usr/bin/env python
# Name: Pascalle Veltman
# Student number: 11025646
"""
This script clearifies given important data about countries.

The data GDP data of Suriname is considered unrealistic and therefore
removed from the GDP data.
"""

import csv
import pandas as pd
import numpy as np
import statistics
from statistics import mean
from statistics import median
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# define file for input
input_csv = "input.csv"
output_json = "output.json"

def main(input):

    df = pd.read_csv(input)
    df1 = df[['Country', 'Region', 'Pop. Density (per sq. mi.)', 'Infant mortality (per 1000 births)', 'GDP ($ per capita) dollars']]
    df1 = df1.stack().str.replace(',','.').unstack()
    countries = df1['Country']
    regions = df1['Region']
    pop_densities = df1['Pop. Density (per sq. mi.)']
    inf_mortalities = df1['Infant mortality (per 1000 births)']
    gdps = df1['GDP ($ per capita) dollars']

    for pop_density in pop_densities:
        if not pop_density or pop_density == "unknown":
            pop_density = None
        else:
            pop_density = float(pop_density)

    for inf_mortality in inf_mortalities:
        if not inf_mortality or inf_mortality == "unknown":
            inf_mortality = None
        else:
            inf_mortality = float(inf_mortality)

    for gdp in gdps:
        print(gdp)
        if not gdp or gdp == "unknown":
            gdp = None
        elif type(gdp) == 'str':
            print(type(gdp))
            gdp = gdp.replace(" dollars","")
            gdp = float(gdp)

    print(gdps)

    # find central tendency example values of GDP
    central_tendency(gdps)

def central_tendency(input):

    # create a list of gdps without "None" and outliers
    input_floats = []
    for gdp in input:
        if gdp is not None and gdp < 400000:
            input_floats.append(gdp)

    # calculate the mean, median and mode of GDP and print it
    mean_input = mean(input_floats)
    print("The mean of the GDP data is: ",mean_input)
    median_input = median(input_floats)
    print("The median of the GDP data is: ",median_input)
    mode_input = statistics.mode(input_floats)
    print("The mode of the GDP data is: ",mode_input)

    # calculate the standard of the GDP data and print it
    std_input = statistics.stdev(input_floats)
    print("The standard dev of GDP is: ",std_input)

    # create a histogram of the GDP data without outliers
    bins = np.arange(0, max(input_floats), max(input_floats)/50)
    plt.xlim(0, max(input_floats))
    plt.hist(input_floats, bins = bins, alpha = 0.5)
    plt.xlabel('GDP ($ per capita) class')
    plt.ylabel('Amount of countries')
    plt.title('GDP of countries (without outliers)')
    plt.savefig("GDP_histogram_without_outliers.png")
    plt.show()

if __name__ == "__main__":
    main(input_csv)
