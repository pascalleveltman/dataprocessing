#!/usr/bin/env python
# Name: Pascalle Veltman
# Student number: 11025646
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_all = {}
data_average = {}
# data_dict_all = {str(key): [] for key in range(START_YEAR, END_YEAR)}
# data_dict_av = {str(key): [] }

def imp_csv(file):
    with open(file) as movies:
        movies_reader = csv.reader(movies, delimiter = ",")
        itermovies = iter(movies_reader)
        next(itermovies)
        for line in itermovies:
            # save year and ranking
            movie_rank = line[1]
            movie_year = int(line[2])
            print(line[1])
            print(line[2])
            # combine and at to dictionary of specific yer
            data_all.setdefault(movie_year, [])
            data_all[movie_year].append(movie_rank)

    # Calculate average rating from movies per year
    for y, r in data_all.items():
        movie_year = y
        data_average.setdefault(movie_year, [])
        length = len(r)
        r = [float(i) for i in r]
        y = int(y)
        print(r)
        data_average[movie_year] = sum(r)/float(length)
        print(data_average)

    # Create x-axis and y-axis
    x = list(range(START_YEAR, END_YEAR))
    print(x)
    y = [data_average[average] for average in x]
    print(y)

    # plot the average rank for each Year
    plt.plot(x, y)
    plt.xlabel('Year of Release')
    plt.ylabel('Average ranking')
    plt.show()

    return True

if __name__ == "__main__":
    imp_csv(INPUT_CSV)
