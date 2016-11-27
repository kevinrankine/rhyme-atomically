from scraper import GeniusScraper
import sys

def main():
    scraper = GeniusScraper('http://rap.genius.com')
    scraper.generate_lyrics_dir(sys.argv[1])

if __name__ == '__main__':
    main()
