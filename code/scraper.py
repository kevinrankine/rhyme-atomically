import requests
from bs4 import BeautifulSoup
import os

class GeniusScraper(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_lyrics(self, song_url):
        page = requests.get(song_url)
        soup = BeautifulSoup(page.text)
        
        lyrics_tag = soup.find_all('lyrics')
        
        if len(lyrics_tag) > 0:
            lyrics = lyrics_tag[0].text
            return lyrics
        
        return None

    def get_songs(self, album_url):
        page = requests.get(album_url)
        soup = BeautifulSoup(page.text)

        songs = map(lambda x : '-'.join(x.text.split(' ')),
                     soup.find_all('span', {"class" : "song_title"}))
        return songs

    def get_albums(self, artist_url):
        page = requests.get(artist_url)
        soup = BeautifulSoup(page.text)
        return map(lambda x : x.text.split('\n')[1].strip(), soup.find_all('div', {"class" : 'vertical_album_card-info'}))

        #print map(lambda x : x["href"], soup.find_all('a', {"class" : "mini_song_card"}))
        #return map(lambda x : x["title"], filter(lambda x : 'lyrics' not in x["href"], soup.find_all('a', {"class" : "mini_song_card"})))

    def generate_lyrics_dir(self, artist):
        artist_url = self.base_url + '/artists/' + artist
        
        ## TODO : get albums
        albums = self.get_albums(artist_url)
        
        songs = []
        
        for album in albums:
            album_url = "%s/albums/%s/%s" % (self.base_url, '-'.join(artist.split(' ')), '-'.join(album.split(' ')))
            album_url = filter(lambda char : char != "'", album_url)
            
            songs = songs + self.get_songs(album_url)
        
        song_urls = map(lambda x : "%s/%s-%s-lyrics" % (self.base_url, '-'.join(artist.split(' ')), x), songs)

        song_lyrics = map(self.get_lyrics, song_urls)

        os.mkdir('./lyrics/' + artist)

        for ii in xrange(len(song_urls)):
            if song_lyrics[ii] is not None:
                f = open("./lyrics/%s/%s.txt" % (artist, songs[ii]), 'w+')
                f.write(song_lyrics[ii].encode('utf-8'))
                f.close()
        

    
