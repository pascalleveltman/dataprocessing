#!/usr/bin/env python
# Name: Pascalle Veltman
# Student number: 11025646
"""
This script scrapes ...
"""

import csv
import pandas as pd
import numpy as np
import statistics
from statistics import mean
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Define file for input
input_csv = "input.csv"

def main(input):

    # Open the file and scan input
    with open(input) as input_file:
        countries_reader = csv.DictReader(input_file)

        # make list with the information per Country
        df_all = []

        # make list for info types
        countries = []
        regions = []
        pop_densities = []
        inf_mortalities = []
        gdps = []

        for row in countries_reader:
            # define information and add to lists of all and info type
            country = row['Country']
            countries.append(country)

            region = row['Region']
            regions.append(regions)

            pop_density = row['Pop. Density (per sq. mi.)']
            if not pop_density or pop_density == "unknown":
                pop_density = None
            else:
                pop_density = pop_density.replace(",",".")
                pop_density = float(pop_density)
            pop_densities.append(pop_density)

            inf_mortality = row['Infant mortality (per 1000 births)']
            if not inf_mortality or inf_mortality == "unknown":
                inf_mortality = None
            else:
                inf_mortality = inf_mortality.replace(",",".")
                inf_mortality = float(inf_mortality)
            inf_mortalities.append(inf_mortality)

            gdp = row['GDP ($ per capita) dollars']
            if not gdp or gdp == "unknown":
                gdp = None
            else:
                gdp = gdp.replace(" dollars","")
                gdp = float(gdp)
            gdps.append(gdp)

            # add information to countries list
            line = [country, region, pop_density, inf_mortality, gdp]
            df_all.append(line)
            # print(line)

        return inf_mortalities
        # return gdps

def histogram(input):
        # create a list of gdps without "none"
        input_floats = [x for x in input if x is not None]
        print(input_floats)
        # calculate the standard deviation of GDP
        std_input = statistics.stdev(input_floats)
        mean_input = sum(input_floats) / len(input_floats)
        # create a histogram for the gdp
        bins = np.arange(0, max(input_floats), max(input_floats)/50)
        plt.xlim(0, max(input_floats))
        plt.hist(input_floats, bins = bins, alpha = 0.5)
        plt.xlabel('GDP class (per 10000 dollars)')
        plt.ylabel('Amount of countries')
        plt.title('GDP $ per capita dollars of countries (with outliers)')
        plt.show()


        # make a list withut outliers
        min_outlier = mean_input - 2 * std_input
        max_outlier = mean_input + 2 * std_input
        for number in input_floats:
            if number < min_outlier or number > max_outlier:
                print(number)
                input_floats.remove(number)
        # create a histogram for the gdp
        bins = np.arange(0, max(input_floats), max(input_floats)/50)
        plt.xlim(0, max(input_floats))
        plt.hist(input_floats, bins = bins, alpha = 0.5)
        plt.xlabel('GDP class (per 1000 dollars)')
        plt.ylabel('Amount of countries')
        plt.title('GDP $ per capita dollars of countries (without outliers)')
        plt.show()

def boxplot(input):
    # delete the empty elements from the list
      input_floats = [x for x in input if x is not None]
      print(input_floats)
      print(type(input_floats))
      # calculate the standard deviation of input
      std_input = statistics.stdev(input_floats)
      print(type(len(input_floats)))
      print(type(sum(input_floats)))
      mean_input = sum(input_floats) / len(input_floats)

      # boxplot with outliers
      plt.boxplot(input_floats)
      plt.title('Infant mortality (per 1000 births) with outliers')
      plt.show()

      # make a list withut outliers
      min_outlier = mean_input - 2 * std_input
      max_outlier = mean_input + 2 * std_input
      for number in input_floats:
          if number < min_outlier or number > max_outlier:
              print(number)
              input_floats.remove(number)
      plt.boxplot(input_floats)
      plt.title('Infant mortality (per 1000 births) without outliers')
      plt.show()


if __name__ == "__main__":
    datafr = main(input_csv)
    # histogram(datafr)
    boxplot(datafr)
