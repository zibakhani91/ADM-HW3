
# coding: utf-8

# In[2]:

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
from queries import *
from voc_ii_creation import *
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt


# In[3]:

def prepro_all(tsvfile):
    tokenizer = RegexpTokenizer(r'\w+') #object to generate tokens(in this case words) and punctuation is removed
    ps = PorterStemmer()#object to stem to tokens and lowercase words
    stop_words = set(stopwords.words('english')) #set with the english stopwords considered
    #Prepocessing documents with all the columns
    for i in range(1,len(tsvfile)+1):
        #loop to preprocess all the documents
        #open and read each document with one entry of the database
        file = open('C:/Users/Jose Manuel Camacho/Desktop/ADMHW3/documents/doc_' + str(i) + '.tsv',encoding='utf-8') 
        line = file.read()
        words = word_tokenize(line) #generate tokens by seperating spaces
        words_witout_stop_words = ["" if word in stop_words else word for word in words]#list with the tokens with no stop words
        new_words = " ".join(words_witout_stop_words).strip()#put togeher the words_without_stops_words
        b = tokenizer.tokenize(new_words) #remove puntuaction and lowercase tokens
        c = []
        for word in b:
            #loop to stem and lowercase all the words  
            c.append(ps.stem(word))
        #creates new file where it is saved all the text preprocessed
        appendFile = open('C:/Users/Jose Manuel Camacho/Desktop/ADMHW3/new_documents/doci_' + str(i) +'.tsv','w',encoding='utf-8')
        appendFile.write(' '.join(c))
        appendFile.close()

def prepro_col(tsvfile):
    tokenizer = RegexpTokenizer(r'\w+') #object to generate tokens(in this case words) and punctuation is removed
    ps = PorterStemmer()#object to stem to tokens and lowercase words
    stop_words = set(stopwords.words('english')) #set with the english stopwords considered
        #Prepocessing documents with description and title
    for i in range(1,len(tsvfile)):
        #loop to preprocess all the documents
        #open and read each document with one entry of the database
        file = open('C:/Users/Jose Manuel Camacho/Desktop/ADMHW3/definitive/doc_' + str(i) + '.tsv',encoding='utf-8') 
        line = file.read()
        words = word_tokenize(line) #generate tokens by seperating spaces
        words_witout_stop_words = ["" if word in stop_words else word for word in words]#list with the tokens with no stop words
        new_words = " ".join(words_witout_stop_words).strip()#put togeher the words_without_stops_words
        b = tokenizer.tokenize(new_words) #remove puntuaction and lowercase tokens
        c = []
        for word in b:
            #loop to stem and lowercase all the words  
            c.append(ps.stem(word))
        #creates new file where it is saved all the text preprocessed
        appendFile = open('C:/Users/Jose Manuel Camacho/Desktop/ADMHW3/definitive_1/doci_' + str(i) +'.tsv','w',encoding='utf-8')
        appendFile.write(' '.join(c))
        appendFile.close()


