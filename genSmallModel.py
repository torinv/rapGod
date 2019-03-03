from __future__ import print_function
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint
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
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


def train_model(**args):
    seqLength = 40
    seqStep = 3
    epochs = 30
    
    #read lyrics and get chars
    text = readLyrics('lyrics_filtered.txt')  
    chars = sorted(list(set(text)))


    #Make input sequences
    #create next_chars array for labeling
    sequences = []
    next_chars = []
    for i in range(0, len(text) - seqLength, seqStep):
        sequences.append(text[i: i + seqLength])
        next_chars.append(text[i + seqLength])


    char_to_index = dict((c, i) for i, c in enumerate(chars))


    #vectorise characters and strings
    X = np.zeros((len(sequences), seqLength, len(chars)), dtype=np.bool)
    y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sequences):
        for t, char in enumerate(sentence):
            X[i, t, char_to_index[char]] = 1
        y[i, char_to_index[next_chars[i]]] = 1


    #model struct
    model = build_model(seqLength, chars)

    fpmodelcheckpoint = "model-{epoch:02d}.h5"
    checkpoint = ModelCheckpoint(fpmodelcheckpoint, monitor='val_acc', verbose=1, save_best_only=False, mode='max')
    callbacks_list = [checkpoint]
    #train
    model.fit(X, y, batch_size=128, nb_epoch=epochs, callbacks=callbacks_list)  


    model.save('skiModelTheSlumpGod.h5')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    arguments = args.__dict__
    
    train_model(**arguments)
