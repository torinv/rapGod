from __future__ import print_function
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import io
import datetime
import argparse
import random
import sys


def readLyrics(path):
    with io.open(path, 'r', encoding='utf8') as f:
        return f.read().lower()

def build_model(sequence_length, chars):
    model = Sequential()
    model.add(LSTM(128, input_shape=(sequence_length, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model


def train_model(**args):
    seqLength = 40
    seqStep = 3
    epochs = 25
    diversity = 1.0
    lyricsPath = "skiMaskTextSlumpGod.txt"
    
    #read lyrics and get chars
    text = readLyrics(lyricsPath)  
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
    model = build_model(seqLength, chars)

    #read
    model = load_model("skiModelTheSlumpGod.h5")

    
    for diversity in [.35]:
        print()
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





if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    arguments = args.__dict__
    
    train_model(**arguments)
