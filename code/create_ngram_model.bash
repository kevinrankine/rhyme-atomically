python preprocess.py ./data/lyrics.txt ./data/processed-lyrics.txt
lmplz -o $1 < ./data/processed-lyrics.txt > ./data/lyrics.arpa
build_binary ./data/lyrics.arpa data/lyrics.klm
