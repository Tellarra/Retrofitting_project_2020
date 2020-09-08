import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from scipy import stats
import scipy
import sys
import argparse

def read_data(file) :
	""" Lit un fichier de mots et leur évaluation humaine de similarité 
	et retourne un dictionnaire type {(mot1, mot2) : évaluation}
	"""
	stream = open(file)
	dico_similarite = {}
	line = stream.readline()

	while line :

		(mot_1, mot_2) = line.split()[0],line.split()[1]
		dico_similarite[(mot_1, mot_2)] = float(line.split()[2])

		line = stream.readline()    

	return dico_similarite


def indice_simil(liste_simil, tri) :
	#pour chaque élement de la liste de similarité, on met son indice+1 (= son rang) dans la liste de rang
	rank = []
	for score in liste_simil : 
		index = 1 + tri.index(score)
		rank.append(index)

	return rank

def coef_spearman(embeddings, data) :
	"""
		Méthode qui va calculer le coefficient de spearman 
	Entrée 
		- embeddings : dictionnaire des embeddings qu'on veut tester
		- data : dictionnaire des paires de mots et de leur similarité évaluée par les humains
		- nb_paires : int du nombre de paires sur lesquelles on veut travailler

		Sortie : coeffitient spearman

	"""
	cos_score = []
	human_score = []
	human_rank = []


	paires = list(data.keys())
	liste_mots = []
	
	#pour chaque paire de mots dont on a les embeddings
	for elt in paires :

		if elt[0] in embeddings and elt[1] in embeddings :
			#on récupère le score humain
			human_score.append(data[elt])


			mot_1,mot_2 = elt[0],elt[1]
			embedding_1 = embeddings[mot_1]
			embedding_2 = embeddings[mot_2]
		
			#on récupère la similarité cossinus
			dot_product = np.dot(embedding_1, embedding_2)
			norm_1 = np.linalg.norm(embedding_1)
			norm_2 = np.linalg.norm(embedding_2)
			cos = dot_product / (norm_1 * norm_2)
			cos_score.append(cos)
		

	#on trie les listes de similarité cos et de l'évaluation humaine
	cos_trie = sorted(cos_score, reverse = True)
	human_trie = sorted(human_score, reverse = True)

	cos_rank = indice_simil(cos_score, cos_trie)
	human_rank = indice_simil(human_score, human_trie)

	#calcul du coefficient de pearsonr
	pearson = scipy.stats.pearsonr(human_rank, cos_rank)
	

	return(pearson)