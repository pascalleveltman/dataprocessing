#!/usr/bin/env python
# Name: Pascalle Veltman
# Student number: 11025646
"""
This script clearifies given important data about countries.
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

# Define file for input
input_csv = "input.csv"
output_json = "output.json"

def main(input):

    # Open the file and scan input
    with open(input) as input_file:
        countries_reader = csv.DictReader(input_file)

        # make list with the information per Country
        dataframe_all = []

        # make list for info types
        countries = []
        regions = []
        pop_densities = []
        inf_mortalities = []
        gdps = []

        for row in countries_reader:

            # define information and add to lists of all and info type
            country = row['Country']
            country = country.strip()
            countries.append(country)

            region = row['Region']
            region = region.strip()
            regions.append(regions)

            # make floats of numbers and change unknown to None
            pop_density = row['Pop. Density (per sq. mi.)']
            if not pop_density or pop_density == "unknown":
                pop_density = None
            else:
                pop_density = pop_density.replace(",",".")
                pop_density = float(pop_density)
            pop_densities.append(pop_density)

            # make floats of numbers and change unknown to None
            inf_mortality = row['Infant mortality (per 1000 births)']
            if not inf_mortality or inf_mortality == "unknown":
                inf_mortality = None
            else:
                inf_mortality = inf_mortality.replace(",",".")
                inf_mortality = float(inf_mortality)
            inf_mortalities.append(inf_mortality)

            # make floats of numbers and change unknown to None
            gdp = row['GDP ($ per capita) dollars']
            if not gdp or gdp == "unknown":
                gdp = None
            else:
                gdp = gdp.replace(" dollars","")
                gdp = float(gdp)
            gdps.append(gdp)

            # add information to countries list
            line = [country, region, pop_density, inf_mortality, gdp]
            dataframe_all.append(line)
            # make sure the preprocessed data is printed
            print(line)

        # find interesting GDP values and plot histogram
        histogram(gdps)

        # find interesting inf_mort values and plot boxplot
        boxplot(inf_mortalities)

        # create java output file by calling function
        json_output(dataframe_all)

def histogram(input):

        # create a list of gdps without "none"
        input_floats = [x for x in input if x is not None]

        # calculate the standard deviation, mean and median of GDP
        std_input = statistics.stdev(input_floats)
        mean_input = sum(input_floats) / len(input_floats)
        median_input = median(input_floats)
        mode_input = statistics.mode(input_floats)
        print("The mean GDP is: ",mean_input)
        print("The median GDP is: ",median_input)
        print("The mode GDP is: ",mode_input)
        print("The standard dev of GDP is: ",std_input)

        # create a histogram for the gdp with outliers
        bins = np.arange(0, max(input_floats), max(input_floats)/50)
        plt.xlim(0, max(input_floats))
        plt.hist(input_floats, bins = bins, alpha = 0.5)
        plt.xlabel('GDP ($ per capita) class')
        plt.ylabel('Amount of countries')
        plt.title('GDP of countries (with outliers)')
        plt.savefig("GDP_histogram_with_outliers.png")
        plt.show()

        # remove possible outliers from list
        min_outlier = mean_input - 2 * std_input
        max_outlier = mean_input + 2 * std_input
        for number in input_floats:
            if number < min_outlier or number > max_outlier:
                input_floats.remove(number)

        # create a histogram for the GDP without ouliers
        bins = np.arange(0, max(input_floats), max(input_floats)/50)
        plt.xlim(0, max(input_floats))
        plt.hist(input_floats, bins = bins, alpha = 0.5)
        plt.xlabel('GDP ($ per capita) class')
        plt.ylabel('Amount of countries')
        plt.title('GDP of countries (without outliers)')
        plt.savefig("GDP_histogram_without_outliers.png")
        plt.show()

def boxplot(input):

      # delete the empty elements from the list
      input_floats = [x for x in input if x is not None]

      # calculate the standard deviation, mean and median of input
      std_input = statistics.stdev(input_floats)
      mean_input = sum(input_floats) / len(input_floats)
      max_input = max(input_floats)
      min_input = min(input_floats)
      median_input = median(input_floats)
      quantile1_input = np.percentile(input_floats, 25)
      quantile3_input = np.percentile(input_floats, 75)
      print("The minimum infant mortality is: ",min_input)
      print("The first quantile of the infant mortality is: ",quantile1_input)
      print("The median infant mortality is: ",median_input)
      print("The third quantile of the infant mortality is: ",quantile3_input)
      print("The maximum infant mortality is: ",max_input)

      # boxplot with outliers
      plt.boxplot(input_floats)
      plt.title('Infant mortality with outliers')
      plt.ylabel('Number of deaths (per 1000 births)')
      plt.savefig("Inf_mort_boxplot_with_outliers.png")
      plt.show()

      # make a list without outliers
      min_outlier = mean_input - 2 * std_input
      max_outlier = mean_input + 2 * std_input
      for number in input_floats:
          if number < min_outlier or number > max_outlier:
              input_floats.remove(number)
      # plot a boxplot without outliers
      plt.boxplot(input_floats)
      plt.title('Infant mortality without outliers')
      plt.ylabel('Number of deaths (per 1000 births)')
      plt.savefig("Inf_mort_boxplot_with_outliers.png")
      plt.show()

def json_output(input):

    # define input
    data = input

    # create dictionary
    json_dict = {}

    # organize data line by line
    for row in data:
        for i in row:
            temp_dict = {}
            temp_dict["Region"] = row[1]
            temp_dict["Pop. Density (per sq. mi.)"] = row[2]
            temp_dict["Infant mortality (per 1000 births)"] = row[3]
            temp_dict["GDP ($ per capita) dollars"] = row[4]
        json_dict[row[0]] = temp_dict

    # create json file
    with open(output_json, 'w') as output_file:
        json.dump(json_dict, output_file)

if __name__ == "__main__":
    datafr = main(input_csv)
