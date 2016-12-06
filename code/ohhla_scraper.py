import os
import re
import requests
from bs4 import BeautifulSoup
import sys

ALL_URLS = map(lambda x : "http://ohhla.com/all%s.html" % x, ['', '_two', '_three', '_four', '_five'])
FAV_URL = "http://ohhla.com/favorite.html"
BASE_URL = "http://ohhla.com/"


class OHHLAScraper(object):
    def __init__(self):
        pass
    
    def get_song(self, song_url):
        soup = BeautifulSoup(requests.get(song_url).text, "lxml")
        song = soup.find_all('pre')

        if len(song) == 0:
            return None
        else:
            return song[0].text

    def get_song_urls(self, artist_url):
        soup = BeautifulSoup(requests.get(artist_url).text, "lxml")
        song_urls = soup.find_all('a')
        song_urls = filter(lambda x : 'href' in x.attrs, song_urls)
        song_urls = map(lambda x : BASE_URL + x['href'], song_urls)
        
        song_urls = filter(lambda x : 'anonymous' in x, song_urls)

        return song_urls
    
    def get_artist_urls(self):
        soup = BeautifulSoup(requests.get(FAV_URL).text, "lxml")

        artist_urls = map(lambda x : BASE_URL + x["href"], soup.find_all('a')[17:-2])

        return artist_urls

    def scrape(self):
        artist_urls = self.get_artist_urls()
        outfile = open('lyrics.txt', 'w')

        for artist_url in artist_urls:
            print artist_url
            song_urls = self.get_song_urls(artist_url)

            for song_url in song_urls:
                song_text = self.get_song(song_url)
                if song_text is not None:
                    song_text = song_text.encode('utf-8')
                    outfile.write(song_text + '\n<NEWSONG>\n')

    def scrape_artist(self, artist_url):
        outfile = open('./%s.txt' % artist_url.split(".com")[1], 'w')

        song_urls = self.get_song_urls(artist_url)

        for song_url in song_urls:
            song_text = self.get_song(song_url)
            if song_text is not None:
                song_text = song_text.encode('utf-8')
                outfile.write(song_text + '\n<NEWSONG>\n')
        
    
if __name__ == '__main__':
    scraper = OHHLAScraper()
    scraper.scrape_artist(sys.argv[1])

    
