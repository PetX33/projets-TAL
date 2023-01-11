#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 15:16:16 2022

@author: Perrine
"""

import spacy
import glob
import json
import os

chemin_fichier = '../DATA/*.txt'
liste_modele = ["fr_core_news_lg", "fr_core_news_sm"]  
        
def stocker(path, contenu):
    w = open(path, "w")
    w.write(json.dumps(contenu, indent=2, ensure_ascii=False))
    w.close()
    return path

# Fonction permettant de lire tous les fichiers du corpus
def LireCorpus(path):
    for path in glob.glob(chemin_fichier):
        with open(path, 'r', encoding="utf-8") as fichier:
                texte = fichier.read()
                #print(texte)        
                yield texte, os.path.basename(path) # Renvoyer le nom du fichier en plus du texte


# Tokenisation      
def tokenisation(texte, modele):
    # Charger le modèle de traitement de langage naturel spacy
    nlp = spacy.load(modele)
    # Initialiser une liste pour stocker les tokens
    liste_tok = []
    # Analyser le texte en entrée avec le modèle spacy
    doc = nlp(texte)
    for token in doc:
        liste_tok.append(token.text) # Ajouter les token à la liste token
    # Retourner la liste token
    return liste_tok

# Segmentation Phrases
def segmentation_sent(texte, modele):
    # Charger le modèle de traitement de langage naturel spacy
    nlp = spacy.load(modele)
    # Initialiser une liste pour stocker les phrases
    list_sent = []
    doc = nlp(texte)
    for sent in doc.sents:
        list_sent.append({                  # Ajouter les phrases à la liste phrase en précisant la phrase et le nombre de token dans la phrase
            "phrase": sent.text,
            "nombre_tokens": len(sent)      # Permet de compter le nombre de token par phrase
        })
    # Retourner la liste phrase
    return list_sent

# Token dans Phrases
def tokens_phrases(texte, modele):
    nlp = spacy.load(modele)
    doc = nlp(texte)
    resultats = {}
    
    for i, sent in enumerate(doc.sents):
        n = 0
        # Ajouter les informations sur le segment (phrase)
        # au dictionnaire des résultats
        resultats["Segment_%s"%i] = {
            "Phrase_%s"%n: sent.text,
            "nombre de token": len(sent),
            "Liste de tokens": [token.text for token in sent]
        }
        n += 1
    return resultats

# Entités
def entite(texte, modele):
    # Charger le modèle de traitement de langage naturel spacy
    nlp = spacy.load(modele)
    doc = nlp(texte)
    # Initialiser un dictionnaire pour stocker les entités
    entities = {}  
    # Pour chaque entité dans le texte
    for i, ent in enumerate(doc.ents):  # va permettre de stocker sous la forme du dictionnaire voulu
       # Ajouter l'entité au dictionnaire en tant qu'élément
       # avec deux clés : "Entité" et "Label"
        entities["entité_%s" %i] = {
            "Entité": ent.text,
            "Label": ent.label_
        }
    # Retourner le dictionnaire des entités
    return entities
    
for modele in liste_modele:
    for texte, nom_fichier in LireCorpus(chemin_fichier): # Récupérer le texte et le nom du fichier
        # print(entite(texte, modele))
        resultats = tokens_phrases(texte, modele) # Stocker les résultat de la fonction tokens_phrases dans la variable resultats
        stocker("../DATA/%s_resultats_%s.json"%(nom_fichier,modele), resultats)
        
        entites = entite(texte, modele)  # Stocker les résultat de la fonction entite dans la variable entites
        stocker("../DATA/%s_entites_%s.json" %(nom_fichier,modele), entites)

        