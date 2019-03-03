from __future__ import print_function
import numpy as np
import sys
import os
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import keras
sys.stderr = stderr
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import io
import tensorflow as tf
import datetime
import argparse
import pyttsx3
import random
from tensorflow.python.lib.io import file_io

#KILL ERROR MESSAGES
tf.logging.set_verbosity(tf.logging.FATAL)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def readLyrics(path):
    with io.open(path, 'r', encoding='utf8') as f:
        return f.read().lower()

def sample(preds, temperature=1.0):

    if temperature == 0:
        temperature = 1

    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds.clip(min=0.0000000000001)) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def train_model(**args):
    seqLength = 40
    lyricsPath = "lyrics_filtered.txt"
    
    #read lyrics and get chars
    text = readLyrics(lyricsPath)  
    chars = sorted(list(set(text)))
    '''

    #Make input sequences
    #create next_chars array for labeling
    sequences = []
    next_chars = []
    for i in range(0, len(text) - seqLength, seqStep):
        sequences.append(text[i: i + seqLength])
        next_chars.append(text[i + seqLength])

    '''
    char_to_index, indices_char = dict((c, i) for i, c in enumerate(chars)), dict((i, c) for i, c in enumerate(chars))
    '''

    #vectorise characters and strings
    X = np.zeros((len(sequences), seqLength, len(chars)), dtype=np.bool)
    y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sequences):
        for t, char in enumerate(sentence):
            X[i, t, char_to_index[char]] = 1
        y[i, char_to_index[next_chars[i]]] = 1


    #model struct
    model = build_model(seqLength, chars)
    '''
    #read
    model = load_model("model-30.h5")

    f = open("output.txt", "w")

    verse = 1
    for diversity in [0.35]: # Change this number for diversity
        print()
        generated = ''
        verse = random.randint(1, 10)

        if verse == 1:
            sentence = "I got hoes calling a young brother phone"
        elif verse == 2:
            sentence = "Young rapGod and Im getting really rich "
        elif verse == 3:
            sentence = "Goin on you with the pick and roll Young"
        elif verse == 4:
            sentence = "Shes in love with who I am Back in high "
        elif verse == 5:
            sentence = "Kiki do you love me Are you riding Say y"
        elif verse == 6:
            sentence = "Its everyday bro with the Disney Channel"
        elif verse == 7:
            sentence = "I got loyalty got royalty inside my DNA "
        elif verse == 8:
            sentence = "I get those goosebumps every time yeah y"
        elif verse == 9:
            sentence = "Draco got that kickback when I blow that"
        else:
            sentence = "I am the one dont weigh a ton Dont need "
        sentence = sentence.lower()
        generated += sentence
        sys.stdout.write(generated)
        print(generated, file=f, end="")

        for i in range(2000): # Change this range to generate more characters
            x = np.zeros((1, seqLength, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_to_index[char]] = 1.

            predictions = model.predict(x, verbose=0)[0]
            next_index = sample(predictions, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            print(next_char, file=f, end="")
            print(next_char, end="")
            sys.stdout.flush()
        print()
        print()
        f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    arguments = args.__dict__
    
    train_model(**arguments)
    # This stuff reads the output out loud
    engine = pyttsx3.init(driverName="nsss")
    engine.say(file_io.read_file_to_string("output.txt"))

    engine.runAndWait()