#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import argparse
import sys
import torch
import torch.nn as nn
import numpy as np
from nltk.corpus import wordnet as wn

def read_examples(file) :
    """ Lit un fichier d'exemples 
    et retourne une liste d'instances de Example
    """
    stream = open(file)
    dico_vect = {}
    line = stream.readline()
    
    while line :
        
        if line.count(" ") > 2 :
            dico_vect[line.split()[0]] = np.array(line.split()[1:len(line)], float)

        line = stream.readline()    

    return dico_vect

# Je sais pas si on en a vraiment besoin du coup
def vect_to_tensors(list_Vect) :
    """
        Méthode qui transforme un vecteur en tenseur
    """
    return torch.tensor(list_Vect)

def fin_word(dico_vector, vector) :
    """
        Méthode qui d'après un vecteur donné
        va retourner son mot correspondant
    """
    for key, value in dico_Vector.items(): 
        if np.sum(vector) == np.sum(value) :
            return key 
  
    return "Le mot n'existe pas ou n'a pas pu être trouvé."

if __name__ == "__main__":

    usage = """ CLASSIFIEUR de DOCUMENTS, de type K-NN

    """+sys.argv[0]+""" [options] EXAMPLES_FILE TEST_FILE

    EXAMPLES_FILE et TEST_FILE sont au format *.examples

    """

    parser = argparse.ArgumentParser(usage = usage)
    parser.add_argument('vector_file', default=None, help='Les vecteurs pré entrainés.')
    #parser.add_argument('test_file', default=None, help='Exemples de test (au format .examples)')
    args = parser.parse_args()

    #------------------------------------------------------------
    # Chargement des exemples d'apprentissage du classifieur KNN
    dico_Vector = read_examples(args.vector_file)
    list_vectors = []

    # Création liste vocab
    vocab = set()
    for key in dico_Vector :
        vocab.add(key)
        list_vectors.append(dico_Vector[key])

    # Transforme les vecteurs en tenseurs
    vect_tens = vect_to_tensors(list_vectors)
    #print(vect_tens)

    # Pour récupérer le mot correspondant au vecteur en question
    print(fin_word(dico_Vector, dico_Vector.get("le")))
    