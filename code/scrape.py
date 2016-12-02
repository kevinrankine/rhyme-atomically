import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import os

from scraper import GeniusScraper

ALL_URLS = map(lambda x : "http://ohhla.com/all%s.html" % x, ['', '_two', '_three', '_four', '_five'])

def main():
    artists = []
    
    #for URL in ALL_URLS:
    # artists = artists + map(lambda x : '-'.join(x.text.split(' ')), BeautifulSoup(requests.get(URL).text, "lxml").find_all('a'))[20:]
    
    URL = "http://ohhla.com/favorite.html"
    artists = map(lambda x : '-'.join(x.text.split(' ')), BeautifulSoup(requests.get(URL).text, "lxml").find_all('a'))[20:]

    for artist in artists:
        try:
            scraper = GeniusScraper('http://rap.genius.com')
            scraper.download_lyrics(artist)
        except(IOError):
            pass
    


main()
