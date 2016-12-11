import sys
import string
import re
from pprint import pprint

PUNCTUATION = '!"#$%&\'()*+,-./:;=?@\\^_`{|}~'
DELIMS = set(['<nv>', '<nl>'])

def is_good_verse(verse):
    cond1 = 'interlude' not in verse.lower() and 'chorus' not in verse.lower() and 'intro' not in verse.lower() and 'outro' not in verse.lower()
    cond2 = len(verse.split('\n')) > 1

    return cond1 and cond2

def is_verse_header(line):
    if re.match('(\[.+\] <nl>)', line):
        return True
    else:
        return False

def split_verses(song):
    verses = re.split('(\[.+\] <nl>)', song)

    return verses

def mark_new_lines(song):
    verses = filter(is_good_verse, song.split('\n\n'))
    song = '\n\n'.join(verses)
    
    lines = song.split('\n')
    lines = map(lambda x : x.strip() + ' <nl>',
                    filter(lambda x : len(x) > 3, lines))
    lines = lines[4:]
    song = ' \n '.join(lines)

    return song

def remove_redundant_tokens(song):
    tokens = song.split(' ')

    ii = 0
    
    while ii < len(tokens):
        a = ii
        while ii < len(tokens) and tokens[ii] in DELIMS:
            ii = ii + 1
        b = ii
            
        if b - a <= 1:
            ii = ii + 1
        else:
            tokens = tokens[:a] + ['<nl>'] + tokens[b:] # used to be <nv> substitution, removing nv char
            ii = a
                
    song = ' '.join(tokens)
    
    return song

def main(in_file, out_file):
    songs = in_file.read().split('\n<NEWSONG>\n')

    for song in songs:
        song = mark_new_lines(song)
        
        verses = split_verses(song)
        verses = filter(lambda x : not is_verse_header(x), verses)
        verses = filter(lambda x : len(x) > 0, verses)
        
        for verse in verses:
            verse = ' '.join(verse.split('\n')) # makes the verse into a single line
            verse = ' '.join(verse.split()) # convert all wsp to single wsp
            verse = verse.strip() # remove leading or training wsp
            verse = verse.translate(None, PUNCTUATION).lower()

            verse = remove_redundant_tokens(verse)
            verse = '<nv> ' + verse + ' <nv>'

            print verse
            print
            
            out_file.write(verse + ' \n')
        

if __name__ == '__main__':
    in_file = open(sys.argv[1], 'r')
    out_file = open(sys.argv[2], 'w')
    
    main(in_file, out_file)
