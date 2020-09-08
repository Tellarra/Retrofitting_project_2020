#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import sys
import torch
import torch.nn as nn
import numpy as np
from nltk.corpus import wordnet as wn
import tache_similarite as ts
import os



#Variable gloable
LIST_NEIGHB = []
VOCAB = set()

def read_examples(file) :
    """ Lit un fichier d'exemples 
    et retourne une liste d'instances de Example
    """
    stream = open(file, encoding='utf-8')
    dico_vect = {}
    line = stream.readline()
    
    while line :
        
        if line.count(" ") > 2 :
            dico_vect[line.split()[0]] = np.asarray(line.split()[1:len(line)], dtype='float32')
        line = stream.readline()    

    return dico_vect

# Je sais pas si on en a vraiment besoin du coup
def vect_to_tensors(list_Vect) :
    """
        Méthode qui transforme un vecteur en tenseur
    """
    return torch.tensor(list_Vect)

def find_vector(dico_vector, word) :
    """
        Méthode qui d'après un vecteur donné
        va retourner son mot correspondant
    """
    for key, value in dico_Vector.items(): 
        if word == key :
            return value 
  
    return "Le mot n'existe pas ou n'a pas pu être trouvé."

def get_neighb(word, language, relation) :
    """
        Méthode qui renvois la liste des voisins
        du mot demandé dans la langue demandée
        avec les relations demandées.
    """
    #print(VOCAB)
    if LIST_NEIGHB != [] :
        LIST_NEIGHB.clear()
    if wn.synsets(word, lang=language) != [] :
        for synset in wn.synsets(word, lang=language) :
            #print(word)
            #print('synset 1 ', synset)
            if relation == 'hypernym' :
                get_lemmas(synset.hypernyms(), language)
            elif relation == 'hyponym' :
                get_lemmas(synset.hyponyms(), language)
            else :
                synset = synset.lemma_names(language)
                #print('synom 2 ', synset)

                for syn in synset :
                    #print('here 222')
                    #print(syn)
                    
                    if syn in VOCAB and syn not in LIST_NEIGHB :
                        #print("here 333")
                        LIST_NEIGHB.append(syn)
                        #print('liste 1 ', LIST_NEIGHB)
    #print('synset ou pas ', wn.synsets(word, lang=language) != [])        
    #print('list 2 ',LIST_NEIGHB)
    return LIST_NEIGHB

def get_lemmas(list_Synset, language) :
    """
        Méthode qui ajoute une liste
        des relations demandées (hyponyme ou hyperonyme)
        à la liste des voisins
    """
    for synset in list_Synset :
        lemmas = synset.lemma_names(language)
        for lemms in lemmas :
            if lemms in VOCAB and lemms not in LIST_NEIGHB :
                LIST_NEIGHB.append(lemms)

def retrofitting (data, nb_epoch, language, relation):
        
    new_data = data
    
    for i in range(nb_epoch) :
            for word in data :
                    new_vector = []
                    get_neighb(word,language, relation)
                    sum_beta = 0
                    #print(LIST_NEIGHB)
                    if LIST_NEIGHB != [] :
                        neighbor_list_size = len(LIST_NEIGHB)
                        new_vector = data[word]
                        for neighbor in LIST_NEIGHB :
                                new_vector += (1/neighbor_list_size)*new_data[neighbor] #(beta*qj)
                                sum_beta +=(1/neighbor_list_size)
                        new_vector = new_vector/(sum_beta+1) #beta*qj/somme beta + 1
                        new_vector = new_data[word]
    return new_data

def retrofitting2 (data, nb_epoch, language, relation):
        
    new_data = data
    
    for i in range(nb_epoch) :
            for word in data :
                    new_vector = []
                    get_neighb(word,language, relation)
                    nb_neighb = len(LIST_NEIGHB)
                    #print(LIST_NEIGHB)
                    if LIST_NEIGHB != [] :
                        new_vector = nb_neighb * data[word]
                        for nghb in LIST_NEIGHB :
                            new_vector += new_data[nghb]
                        new_data[word] = new_vector/(2*nb_neighb)

    return new_data

if __name__ == "__main__":

    usage = """ CLASSIFIEUR de DOCUMENTS, de type K-NN

    """+sys.argv[0]+""" [options] EXAMPLES_FILE TEST_FILE

    EXAMPLES_FILE et TEST_FILE sont au format *.examples

    """

    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument('vector_file', default=None, help='Les vecteurs pré entrainés.')
    parser.add_argument('data_file', default=None, help='Fichier des notes humaines de similarité entre deux mots')
    args = parser.parse_args()

    #------------------------------------------------------------
    # Chargement des vecteur word2vec
    dico_Vector = read_examples(args.vector_file)
    list_vectors = []

    # Création de la liste de vocabulaire
    for key in dico_Vector :
        VOCAB.add(key)
        list_vectors.append(dico_Vector[key])
    
    dico_simil = ts.read_data(args.data_file)

    """
    #-----------------------Avant retrofitting---------------------------
    ############## Tâche de similarité ############

    
    print(ts.coef_spearman(dico_Vector, dico_simil))

    ########## Analyse des sentiments ##########
    import analyse_sentiment as ans
    embedding_matrix = ans.construct_embed(dico_Vector)
    ans.construct_model(embedding_matrix, True)
    ans.train_and_fit()
    """
    
    """
    #---------------- Retrofitting ----------------------------------
    new_data = retrofitting2(dico_Vector, 1, 'fra', 'synonymes')

    #--------------- Après retrofitting ------------------
    ############ Tâche de similarité ##############

    print(ts.coef_spearman(new_data, dico_simil))

    ########## Analyse des sentiments ##########

    embedding_matrix = ans.construct_embed(new_data)
    ans.construct_model(embedding_matrix, True)
    ans.train_and_fit()
    """

    
    

    
    
    
    

    