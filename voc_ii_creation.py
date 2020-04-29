
# coding: utf-8

# In[3]:

import pandas as pd                         #import libraries
import numpy as np
import nltk
import csv
import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import json
from IPython.display import HTML, display
from tabulate import tabulate
from math import log
from numpy import linalg as LA
from heapq import *


# In[4]:

def vocabulary_creation(word_list,previous_vocabulary):
    #create an new dictionary from a previous one which could be empty
    vocabulary=previous_vocabulary
    #obtain last index of previous dictionary and set first index for 1st different element in this vocabulary
    if len(previous_vocabulary)==0:
        number=1
    else:
        number=previous_vocabulary[list(previous_vocabulary)[len(previous_vocabulary)-1]]+1
    #adding new words to the vocabulary and omitting repeated ones
    for word in word_list:
        index=list(vocabulary.keys())
        if word in index:
            pass
        else:
            vocabulary[word]=number
            number+=1
    return vocabulary

def inverted_index_creation(vocabulary,tsvfile):  
    #function that creates inverted_index from all the documents
    inverted_index={}
    n=1
    
    for i in range(1,len(tsvfile)):
         #loop for each word of the document create a new key if the word is not in the dictionary 
         #add the number of the document to an existing key is the word is in the dictionary
        aux=((open('C:/Users/Jose Manuel Camacho/Desktop/ADMHW3/definitive_1/doci_' + str(i) +'.tsv','r',encoding='utf-8')).read()).split(' ')
        for j in set(aux):
            index=list(vocabulary.values())
            if vocabulary[j] in list(inverted_index.keys()):
                inverted_index[vocabulary[j]]=(inverted_index[vocabulary[j]])+['d_'+(str(n))]
            else:
                inverted_index[int(vocabulary[j])]=["d_"+str(n)]
              
        n+=1

            
    with open('inverted_index.tsv', 'w') as f1: #write the inverted index in a file called "inverted_index.tsv"
        json.dump(inverted_index, f1)
        f1.close()
    return inverted_index

#functions defined in order to calculate the tfIdf coefficient
def N(collection):
    #number of documents in the collection
    return len(collection)
def df_t(term,collection):
    #number of documents in the collection that contain a term t
    counter=0
    for lista in collection:
        if term in lista:
            counter+=1
    return counter
def tf_t_d(term,lista):
    #term frequency:number of ocurrence of term t in document d
    return lista.count(term)

def id_f_t(term,collection):
    #inverse document frequency of a term t
    return log(len(collection)/df_t(term,collection),10)
def tf_idf(term,lista,collection):
    #tf_idf of a term in a document of a collection N
    return tf_t_d(term,lista)*id_f_t(term, collection)



def inverted_index_creation_tfIdf(vocabulary,collection):  
    #function that creates inverted_index with coefficient tfIdf from all the documents
    inverted_index={}
    n=1
    
    for lista in collection:          
         #loop for each word of the document create a new key if the word is not in the dictionary 
         #add the number of the document to an existing key is the word is in the dictionary
         #tfIdf coefficient of each term is also added
        for term in set(lista):
    
            index=list(vocabulary.values())
            if vocabulary[term] in list(inverted_index.keys()):
                inverted_index[vocabulary[term]]=(inverted_index[vocabulary[term]])+[("d_"+str(n),tf_idf(term,lista,collection))]
            else:
                inverted_index[int(vocabulary[term])]=[("d_"+str(n),tf_idf(term,lista,collection))]
        
        n+=1

    with open('inverted_index_tfIdf.tsv', 'w') as f1: #write the inverted index in a file called "inverted_index_tfIdf.tsv"
        json.dump(inverted_index, f1)
        f1.close()
    return inverted_index 

