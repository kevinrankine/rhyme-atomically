import sys
import h5py

WORD_VECTOR_FILE = 'data/lyrics_vectors.txt'
LYRICS_FILE = 'data/processed-lyrics.txt'

def load_word_vectors(word_vector_file):
    word_to_index = {}
    word_vectors = []
    
    with open(word_vector_file) as f:
        index = 1
        
        for line in f:
            splitted = line.split()
            word, vector = splitted[0], map(float, splitted[1:])

            word_vectors.append(vector)
            
            word_to_index[word] = index
            index = index + 1

    def mapping(x):
        return word_to_index[x]
    
    return mapping, word_vectors

def main(in_file_name):
    word_to_index, word_vectors = load_word_vectors(WORD_VECTOR_FILE)
    inf = open(in_file_name, 'r')
    
    for song in inf:
        song = song.split()
        song = map(word_to_index, song)
        
        print song
    

if __name__ == '__main__':
    main(LYRICS_FILE)
