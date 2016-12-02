import os
import re
import requests
from bs4 import BeautifulSoup

class GeniusScraper(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_lyrics(self, song_url):
        soup = BeautifulSoup(requests.get(song_url).text, "lxml")
        
        lyrics_tag = soup.find_all('lyrics')
        
        if len(lyrics_tag) > 0:
            lyrics = lyrics_tag[0].text
            return lyrics
        
        return None

    def get_songs(self, album_url):
        soup = BeautifulSoup(requests.get(album_url).text, "lxml")

        songs = map(lambda x : '-'.join(x.text.split(' ')),
                     soup.find_all('span', {"class" : "song_title"}))
        return songs

    def get_albums(self, artist_url):
        soup = BeautifulSoup(requests.get(artist_url).text, "lxml")
        
        return map(lambda x : x.text.split('\n')[1].strip(), soup.find_all('div', {"class" : 'vertical_album_card-info'}))

    def process_lyrics(self, lyrics):
        lyrics = lyrics.encode('utf-8')
        
        verses = re.split('(\[.+\])', lyrics)
        lyrics = '<newVerse>'.join(verses)
        
        lines = map(lambda x : x if x == '<newVerse>' else x + ' <newLine>', lyrics.split('\n'))
        lyrics = '\n'.join(lines)

        return lyrics
    
    def download_lyrics(self, artist):
        artist_url = self.base_url + '/artists/' + artist
        
        albums = self.get_albums(artist_url)
        
        songs = []
        
        for album in albums:
            album_url = "%s/albums/%s/%s" % (self.base_url, '-'.join(artist.split(' ')), '-'.join(album.split(' ')))
            album_url = filter(lambda char : char != "'", album_url)
            
            songs = songs + self.get_songs(album_url)
        
        song_urls = map(lambda x : "%s/%s-%s-lyrics" % (self.base_url, '-'.join(artist.split(' ')), x), songs)

        song_lyrics = map(self.get_lyrics, song_urls)
        song_lyrics = filter(lambda x : x is not None, song_lyrics)
        song_lyrics = map(self.process_lyrics, song_lyrics)
        song_lyrics = '\n'.join(song_lyrics)

        to_remove = re.findall('(\[.+\])', song_lyrics)

        for string in to_remove:
            song_lyrics = song_lyrics.replace(string, "")

        song_lyrics = '\n'.join(filter(lambda s : len(s) > 0, song_lyrics.split('\n')))

        f = open('./lyrics/%s.txt' % artist, 'w')
        
        f.write(song_lyrics)
        
        

    
