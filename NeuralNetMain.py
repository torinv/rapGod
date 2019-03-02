from __future__ import print_function
import helper
import numpy as np
import random
import sys
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import io

#vars
seqLength = 40
seqStep = 3
lyricPath = "test1.txt"
gcsLyricPath = gs://data/test1.txt
epochs = 10
diversity = 1.0

gsutil cp $gcsLyricPath $lyricPath

#read lyrics and get chars
text = helper.readLyrics(lyricPath)
chars = sorted(list(set(text)))


#Make input sequences
#create next_chars array for labeling
sequences = []
next_chars = []
for i in range(0, len(text) - seqLength, seqStep):
    sequences.append(text[i: i + seqLength])
    next_chars.append(text[i + seqLength])


char_to_index, indices_char = dict((c, i) for i, c in enumerate(chars)), dict((i, c) for i, c in enumerate(chars))


#vectorise characters and strings
X = np.zeros((len(sequences), seqLength, len(chars)), dtype=np.bool)
y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sequences):
    for t, char in enumerate(sentence):
        X[i, t, char_to_index[char]] = 1
    y[i, char_to_index[next_chars[i]]] = 1


#model struct
model = helper.build_model(seqLength, chars)

#train
#comment out bottom if training, top two if running trained model
model.fit(X, y, batch_size=128, nb_epoch=epochs)
model.save("modelOutput.h5")
#model = load_model("modelOutput.h5") 


for diversity in [0.2, 0.5, 1.0, 1.2]:
    print()
    print('----- diversity:', diversity)

    generated = ''
#choose random sentence number for seed
    sentenceChoice = random.randint(0, 5)

    if sentenceChoice == 1:
        sentence = "Hey my name is Torin and I'm here to say"
    elif sentenceChoice == 2:
        sentence = "Hey my name is Reed and I'm here to say "
    elif sentenceChoice == 3:
        sentence = "This is not rap, this is just a test of "
    elif sentenceChoice == 4:
        sentence = "This rap was coded, ya better believe it"
    elif sentenceChoice == 5:
        sentence = "I really hope this thing works, starting"

    sentence = sentence.lower()
    generated += sentence

    print('----- Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)

    for i in range(400):
        x = np.zeros((1, seqLength, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_to_index[char]] = 1.

        predictions = model.predict(x, verbose=0)[0]

        temperature=1.0
        preds = predictions
        if temperature == 0:
            temperature = 1
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        next_index = np.argmax(probas)

        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()
