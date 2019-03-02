from __future__ import print_function
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import io
import datetime
import tensorflow as tf
from tensorflow.python.lib.io import file_io
from tensorflow.python.client import device_lib
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


def train_model(train_file='gs://rapgodbucket/halflyrics.txt', job_dir='gs://rapgodbucket/multijobGPU6', **args):
    with tf.device('/device:GPU:0'):
        seqLength = 40
        seqStep = 3
        epochs = 1
        diversity = 1.0
        count = 1
        characters = file_io.read_file_to_string('gs://rapgodbucket/lyrics_filtered.txt')
        chars = sorted(list(set(characters)))
        #model struct
        model = build_model(seqLength, chars)
        

        #read lyrics and get chars
        text = file_io.read_file_to_string('gs://rapgodbucket/lyrics_filtered.txt')
        #gcs_file = gcs.open(train_file)
        #text = gcs_file.read()  
        


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

        #train
        model.fit(X, y, batch_size=256, nb_epoch=epochs)

        model.save('model.h5')
        with file_io.FileIO('model.h5', mode='r') as input_f:
            with file_io.FileIO(job_dir + '/model.h5', mode='w+') as output_f:
                output_f.write(input_f.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Input Arguments
    parser.add_argument(
      '--train-file',
      help='GCS or local paths to training data',
      required=True
    )

    parser.add_argument(
      '--job-dir',
      help='GCS location to write checkpoints and export models',
      required=True
    )
    args = parser.parse_args()
    arguments = args.__dict__
    job_dir = arguments.pop('job_dir')
    
    train_model(**arguments)
