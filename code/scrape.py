import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import os
import sys

from genius_scraper import GeniusScraper

ALL_URLS = map(lambda x : "http://ohhla.com/all%s.html" % x, ['', '_two', '_three', '_four', '_five'])

def main():
    artists = []
    
    URL = "http://ohhla.com/favorite.html"
    artists = map(lambda x : '-'.join(x.text.split(' ')), BeautifulSoup(requests.get(URL).text, "lxml").find_all('a'))[20:]



    if len(sys.argv) == 1:
        f = open('lyrics.txt', 'w')
        
        for artist in artists:
            try:
                scraper = GeniusScraper('http://rap.genius.com')
                lyrics = scraper.get_all_lyrics(artist)
                f.write(lyrics + '\n')
                print artist
            except(IOError):
                pass
    else:
        f = open('%s.txt' % (sys.argv[1]), 'w')
        scraper = GeniusScraper('http://rap.genius.com')
        lyrics = scraper.get_all_lyrics(sys.argv[1])
        f.write(lyrics)
        

main()
