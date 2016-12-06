python preprocess.py ./data/lyrics.txt ./data/processed-lyrics.txt
lmplz -o 4 < ./data/processed-lyrics.txt > ./data/lyrics.arpa
build_binary ./data/lyrics.arpa lyrics.klm
