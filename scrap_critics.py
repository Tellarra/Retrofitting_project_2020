# Import libs
import pandas as pd
import numpy as np
from requests import get
from time import time
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import dateparser
import re
import os
import json

from warnings import warn
from IPython.core.display import clear_output
import traceback

NOTE_DICO = {}


def getMoviesUrl(start_page, end_page):
    """
        Function to scrape the movies urls from http://www.allocine.fr/films/
        Choose the page range with the two parameters start_page and end_page.
        The url list is save as a csv file: movie_url.csv
    """
    # Set the list
    movie_url = []
    
    # Preparing the setting and monitoring of the loop
    start_time = time()
    p_requests = start_page
    m_requests = 0
        
    for p in range(start_page, end_page):

        # Get request
        url = 'http://www.allocine.fr/films/?page={}'.format(str(p))
        response = get(url)
        
        # Pause the loop
        sleep(randint(1,2))
            
        # Monitoring the requests
        elapsed_time = time() - start_time
        print('Page Request: {}; Frequency: {} requests/s'.format(p_requests, p_requests/elapsed_time))
        clear_output(wait = True)
            
        # Warning for non-200 status codes
        if response.status_code != 200:
            warn('Page Request: {}; Status code: {}'.format(p_requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if p_requests > end_page:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        html_soup = BeautifulSoup(response.text, 'html.parser')

        # Select all the movies url from a single page
        movies = html_soup.find_all('h2', 'meta-title')
        m_requests += len(movies)
        
        # Monitoring the requests
        print('Page Request: {}; Movie Request: {}'.format(p_requests, m_requests))
        clear_output(wait = True)
        
        # Pause the loop
        sleep(1)
        
        for movie in movies:
            id_movie = re.findall('\d+', movie.a['href'])
            movie_url.append(f'http://www.allocine.fr/film/fichefilm-{id_movie[0]}/critiques/spectateurs/')
        
        p_requests += 1
    
    # Saving the files
    return np.asarray(movie_url)

# We use it to scrape the first 3999 pages
movie_url = getMoviesUrl(1, 2)

def ScrapeURL(movie_url):
    """
        Function to scrape the data from the movies urls
        The function return a dataframe and a list of url that return error.
        And save them into csv files (allocine_movies.csv and allocine_errors.csv)
    """
    
    # preparing the setting and monitoring loop
    start_time = time()
    n_request = 0
    
    # init list to save errors
    errors = []
    
    note_dico = {}
    # request loop
    for url in movie_url:
        try :
            critic_list = []
            response = get(url)

            # Pause the loop
            sleep(randint(1,2))

            # Monitoring the requests
            n_request += 1
            
            elapsed_time = time() - start_time
            print('Request #{}; Frequency: {} requests/s'.format(n_request, n_request/elapsed_time))
            clear_output(wait = True)

            # Pause the loop
            sleep(randint(1,2))

            # Warning for non-200 status codes
            if response.status_code != 200:
                warn('Request #{}; Status code: {}'.format(n_request, response.status_code))
                errors.append(url)

            # Parse the content of the request with BeautifulSoup
            movie_html_soup = BeautifulSoup(response.text, 'html.parser')
            if movie_html_soup.find('section', 'section'):

                for crit in movie_html_soup.find_all('div','content-txt review-card-content') :
                    critic_list.append(crit.text.strip())

                count_note = 0

                for note in movie_html_soup.find_all('span', 'stareval-note') :
                    note = float(note.text.strip().replace(',','.'))
                    if note <= 2.5 :
                        note = 'negatif'
                    else :
                        note = 'positif'

                    NOTE_DICO[critic_list[count_note]] = note
                    count_note += 1
                    if count_note == len(critic_list) :
                        break
                

        except:
            errors.append(url)
            warn('Request #{} fail; Total errors : {}'.format(n_request, len(errors)))
            traceback.print_exc()
    # monitoring 
    elapsed_time = time() - start_time
    print('Done; {} requests in {} seconds with {} errors'.format(n_request, round(elapsed_time, 0), len(errors)))
    clear_output(wait = True)
    write_to_file(NOTE_DICO)
    
def write_to_file(dico_critique) :
    """
        Méthode qui écris dans un fichier text nos critiques de films avec
        sa polarité associé. Sous format JSON
    """
    path = os.getcwd()
    if os.path.isfile(f'{path}/critic_corpus.txt') :
        critic_corpus = open(f'{path}/critic_corpus.txt', "a", encoding='utf8') 
    else :
        critic_corpus = open(f'{path}/critic_corpus.txt', "w+", encoding='utf8')

    critic_corpus.write(json.dumps(dico_critique, ensure_ascii=False, sort_keys=True))
    critic_corpus.close()

ScrapeURL(movie_url)

