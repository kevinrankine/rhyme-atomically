import sys
import h5py
from nltk.model import build_vocabulary
import numpy as np

WORD_VECTOR_FILE = 'data/lyrics_vectors.txt'
LYRICS_FILE = 'data/processed-lyrics.txt'

def load_word_vectors(word_vector_file, vocab):
    word_to_index = {}
    word_vectors = []
    
    with open(word_vector_file) as f:
        index = 1
        
        for line in f:
            splitted = line.split()
            word, vector = splitted[0], map(float, splitted[1:])

            if word in vocab:
                word_vectors.append(vector)
                
                word_to_index[word] = index
                index = index + 1

    word_to_index['<unk>'] = len(word_to_index) + 1
    word_vectors.append([0 for _ in xrange(len(word_vectors[0]))])

    word_to_index['<pad>'] = len(word_to_index) + 1
    word_vectors.append([0 for _ in xrange(len(word_vectors[0]))])

    def mapping(x):
        if x in word_to_index:
            return word_to_index[x]
        else:
            return word_to_index['<unk>']
    
    return mapping, np.array(word_vectors, dtype=np.float32)

def main(in_file_name):
    sentences = map(lambda x : x.split(' '), open(LYRICS_FILE, 'r').read().split('\n'))
    text = [val for sub in sentences for val in sub]
    text = filter(lambda x : x != '', text)
    
    vocab = set(build_vocabulary(1000, text).keys())
    word_to_index, word_vectors = load_word_vectors(WORD_VECTOR_FILE, vocab)

    inf = open(in_file_name, 'r')

    X = []
    
    for song in inf:
        verses = filter(lambda x : len(x) > 0, song.split('<nv>'))
        
        for verse in verses:
            verse = verse.split()
            verse = map(word_to_index, verse)

            X.append(verse)

    X = filter(lambda x : len(x) <= 500, X)

    max_len = max(map(len, X))
    X = map(lambda x : (max_len - len(x)) * [word_to_index('<pad>')] + x, X)

    print "The mean verse length is %d" % np.mean(map(len, X))
    
    X = np.array(X, dtype=np.int32)
    y = np.array(map(lambda x : x[1:], X), dtype=np.int32)

    with h5py.File('./data/data.hdf5', 'w') as f:
        f['X'] = X
        f['y'] = y
        f['word_vectors'] = word_vectors

if __name__ == '__main__':
    main(LYRICS_FILE)
