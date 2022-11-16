import os

synsets = os.listdir()

word_map = {}
with open("..\\words.txt", "r") as words:
    for line in words.readlines():
        lines_split = line.split("\t")
        word_map[lines_split[0]] = lines_split[1].replace("\n", "")

with open("tiny_labelled_synsets.txt", "w") as labelled_synsets:
    for synset in synsets:
        labelled_synsets.write(synset + "\t" + word_map[synset] + "\n")
