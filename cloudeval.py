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
import random

#KILL ERROR MESSAGES
tf.logging.set_verbosity(tf.logging.FATAL)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

try:
    def readLyrics(path):
        with io.open(path, 'r', encoding='utf8') as f:
            return f.read().lower()


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
        model = load_model("skiModelTheSlumpGod.h5")

            
        for diversity in [.35]:
            print()
            generated = ''
        #choose random sentence number for seed
            sentence = "Hey my name is Torin and Im here to say "
            
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
