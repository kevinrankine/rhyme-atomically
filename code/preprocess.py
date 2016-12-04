import sys
import string
import re

PUNCTUATION = '!"#$%&\'()*+,-./:;=?@\\^_`{|}~'

def mark_new_verses(song):
    brackets = re.findall('(\[.+\] <nl>)', song)
        
    for bracket in brackets:
        song = song.replace(bracket, '<nv> ')

    return song

def mark_new_lines(song):
    lines = map(lambda x : x.strip() + ' <nl>',
                    filter(lambda x : len(x) > 3, song.split('\n')))
    song = '\n'.join(lines)

    return song

def main(in_file, out_file):
    songs = in_file.read().split('\n<NEWSONG>\n')
    
    for song in songs:
        song = mark_new_lines(song)
        song = mark_new_verses(song)

        song = song.translate(None, PUNCTUATION).lower()
        
        song = ' '.join(song.split('\n')) # makes the song into a single line
        song = ' '.join(song.split()) # convert all wsp to single wsp
        song = song.strip() # remove leading or training wsp
        
        song = '<s> ' * 5 + song + ' </s>' * 5 # start/end tags
        
        out_file.write(song + '\n')
        

if __name__ == '__main__':
    in_file = open(sys.argv[1], 'r')
    out_file = open(sys.argv[2], 'w')
    
    main(in_file, out_file)
