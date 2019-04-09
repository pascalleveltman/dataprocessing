#!/usr/bin/env python
# Name: Pascalle Veltman
# Student number: 11025646
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# global dictionary for the data per year
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

# open the csv file with the information
def imp_csv(file):
    with open(file) as movies:
        movies_reader = csv.reader(movies, delimiter = ",")
        itermovies = iter(movies_reader)
        # skip the first line
        next(itermovies)
        for line in itermovies:
            # save year and ranking
            movie_rank = float(line[1])
            movie_year = line[2]
            # combine and at to dictionary of specific yer
            data_dict[movie_year].append(movie_rank)

    # create new dictionary for the averages
    data_average = {}
    for year, ranks in data_dict.items():
        movie_year = int(year)
        data_average.setdefault(movie_year, [])
        length = len(ranks)
        data_average[movie_year] = sum(ranks)/float(length)

    # make a plot with the averages
    x = list(range(START_YEAR, END_YEAR))
    y = [data_average[year] for year in x]

    # plot the average rank for each Year
    plt.plot(x, y)
    plt.xlabel('Year of Release')
    plt.ylabel('Average Ranking')
    plt.title('Average Ranking of Movies on IMDB')
    plt.ylim(1, 10)
    plt.show()

if __name__ == "__main__":
    imp_csv(INPUT_CSV)
