#!/usr/bin/env python
# Name: Pascalle Veltman
# Student number: 11025646
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    # create a general list to add the movies to
    movies = []

    # grabs each item in the ranking list
    containers = dom.findAll("div", {"class":"lister-item mode-advanced"})

    # iterate through the ranking list to save contents
    for container in containers:
        # select div with content
        content = container.find("div", {"class":"lister-item-content"})

        # from the header in content select the title
        title = content.h3.a.text

        # check if there is a komma in title
        if "," in title:
            title = title.replace(",", ";")

        # select the rating of the movie from the rating bar
        rating = content.div.div["data-value"]
        rating = float(rating)

        # select the year of release from the header
        headeryear = content.h3.find("span", {"class":"lister-item-year text-muted unbold"})
        year = headeryear.text

        # remove brackets and check if year is also I or II
        year = year.replace("(","")
        year = year.replace(")","")
        if 'II' in year:
            year = year.replace("II ", "")
            title = title + " II"
        if 'I' in year:
            year = year.replace("I ", "")
            title = title + " I"
        year = int(year)

        # create a list for the actors
        actors = []

        # select actors from content and add to list
        stars = content.findAll('a')
        for star in stars:
            if "_li_st_" in star["href"]:
                name =  star.text
                actors.append(name)
        # replace list by string
        actors = ', '.join(actors)

        # select runtime and make sure it is just a number
        runtime = content.p.find("span", {"class":"runtime"}).text
        runtime = runtime.replace(" min", "")

        # save as list in line and add line to movies
        line = [title, rating, year, actors, runtime]
        movies.append(line)

    # return list of movies
    return (movies)


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])

    for line in movies:
        writer.writerow(line)

    return(writer)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
