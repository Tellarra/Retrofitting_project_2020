#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import sys
import torch
import torch.nn as nn
import numpy as np
from nltk.corpus import wordnet as wn
import tache_similarite as ts
from keras import *
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Dense, LSTM
import pandas as pd
import tensorflow.keras as keras
from sklearn.model_selection import train_test_split

import os.path
import json
from sklearn.feature_extraction import DictVectorizer

EMBEDDING_DIM = 100
MODEL = Sequential()


def get_critics(path_corpus) :
    if os.path.isfile(f'{path_corpus}/critic_corpus.txt') :
        critic_corpus = f'{path_corpus}/critic_corpus.txt'
        
    else :
        import scrap_critics
        critic_corpus = f'{path_corpus}/critic_corpus.txt'

    with open(critic_corpus, 'r') as json_file:
        #print(json_file)
        dico_critics = json.load(json_file)
    #print(dico_critics)

    return dico_critics.keys(), list(dico_critics.values())

def construct_embed(dico_vect) :
    """
        Méthode qui construit les embeddings
    """
    embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        embedding_vector = dico_vect.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector
    
    return embedding_matrix

def construct_model(embedding_matrix, trainable) :
    """
        Méthode qui construit le réseau de neurones LSTM
    """
    MODEL.add(Embedding(len(word_index)+1, EMBEDDING_DIM, weights=[embedding_matrix], trainable=trainable))
    MODEL.add(LSTM(lstm_out, dropout_U = 0.2, dropout_W = 0.2))
    MODEL.add(Dense(2,activation='softmax'))
    MODEL.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
    print(MODEL.summary())
def train_and_fit() :    
    """
        Méthode qui créée et fit le modèle sur nos données d'évaluations.
    """

    Y = pd.get_dummies(SENTIMENT).values
    X_train, X_valid, Y_train, Y_valid = train_test_split(X,Y, test_size = 0.20, random_state = 36)

    MODEL.fit(X_train, Y_train, batch_size=batch_size, nb_epoch = 5,  verbose = 5)
    score,acc = MODEL.evaluate(X_valid, Y_valid, verbose=2, batch_size=batch_size)
    print("Score : ",score)
    print("Accuracy : ",acc)

TEXT, SENTIMENT = get_critics(os.getcwd())

tokenizer = Tokenizer(lower=True,split=' ')
tokenizer.fit_on_texts(TEXT)
X = tokenizer.texts_to_sequences(TEXT)
word_index = tokenizer.word_index
X = pad_sequences(X)

lstm_out = 200
batch_size = 32