import re
import matplotlib.pyplot as plt

def word_count(sentence):
    word_counter = {}
    wordlist = sentence.lower().split()
    for word in wordlist:
        word = re.sub('[.,:*! ]', '', word)

        if word in word_counter:
            word_counter[word] = 1 + word_counter[word]
        else:
            word_counter[word] = 1
    return word_counter

f = open("country_filtered.txt", "r")
outfile = open("wordcount.txt", "w")
words = {}
for line in f:
	print("Gathering line: \"" + line.strip() + "\"")
	words.update(word_count(line))

for word in words:
    regex = re.compile(word)
    print(re.findall(word, f.read()))