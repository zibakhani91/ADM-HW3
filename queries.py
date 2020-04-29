
# coding: utf-8

# In[1]:

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


# In[2]:

def conjunctive_query(vocabulary_load,inv_indx, df):
    
    input_ = input() #input of the user with the query

    #preprocessing of the input
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()
    words = word_tokenize(input_)
    words_without_stop_words = ["" if word in stop_words else word for word in words]
    new_words = " ".join(words_without_stop_words).strip()
    b = tokenizer.tokenize(new_words)
    c = []
    for word in b:
        c.append(ps.stem(word))
    #compute the indexes of the word of the query
    idx=[]
    for word in c:
        idx.append(vocabulary_load[word])
    #execute the query and obtain all the documents which contain all the terms of the query
    idx_results = [inv_indx[str(i)] for i in idx]
    query_result=set.intersection(*map(set, idx_results))
    #create table output
    df3=df[["title","description","city",'url']] #consider dataframe with columns of interest
    lines = [int(i[2:])-1 for i in query_result]#extract numbers of the documents from the result of the query
    #generate table with the outputs
    results = df3.iloc[lines,]
    display(HTML(tabulate(results, headers= ['Title', 'Description','City','Url'], showindex=False, tablefmt="html")))
    
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

def conjunctive_query_cosine(vocabulary_load,inv_indx ,inverted_index_tfIdf,collection, df):
    input_1 = input() #input of the user with the query
    #preprocessing of the input
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()
    words = word_tokenize(input_1)
    words_without_stop_words = ["" if word in stop_words else word for word in words]
    new_words = " ".join(words_without_stop_words).strip()
    b = tokenizer.tokenize(new_words)
    c = []
    for word in b:
        c.append(ps.stem(word))
    idx=[]
    for word in c:
        idx.append(vocabulary_load[word])
    #execute the query and obtain all the documents which contain all the terms of the query
    idx_results = [inv_indx[str(i)] for i in idx]
    query_result=set.intersection(*map(set, idx_results))
    df3=df[["title","description","city",'url']]
    coefficients={}#dictionary with the norm of the document vector 
    dot_prod_coeff_1={} #dot product between query and document
    cosinesimilarity_1={} #dictionary with the cosine similarity for each document and the query
    inputnorm=LA.norm([tf_idf(j,c,collection) for j in set(c)]) #norm of the query;always the same
    for i in query_result: 
        #loop through each document that contains all the words
        document_coef=[]
        dot_product=[]
        repetition_1=[] #list to avoid unwanted repetitions in first conditional
        repetition_2=[] #list to avoid unwanted repetitions in second conditional
        for j in collection[int(i[2:])-1]: 
            #loop through each word of the document of the intersection
            for k in range(len(inverted_index_tfIdf[str(vocabulary_load[j])])):# range each location of the key=document 
                if ( i in inverted_index_tfIdf[str(vocabulary_load[j])][k]) and (j not in repetition_1) :
                    #take all the components of the vector document
                    document_coef.append(inverted_index_tfIdf[str(vocabulary_load[j])][k][1])
                    repetition_1.append(j)


                if (( i in inverted_index_tfIdf[str(vocabulary_load[j])][k]) and vocabulary_load[j] in idx) and (j not in repetition_2):
                   #take all the components needed to compute the dot product
                    dot_product.append((inverted_index_tfIdf[str(vocabulary_load[j])][k][1]*tf_idf(j,c,collection)))
                    repetition_2.append(j) 
        coefficients["document"+str(i)]=LA.norm(document_coef)
        dot_prod_coeff_1["document"+str(i)]=sum(dot_product)
        cosinesimilarity_1[str(i)]=dot_prod_coeff_1["document"+str(i)]/(inputnorm*coefficients["document"+str(i)])
    lines_1 = [int(i[2:])-1 for i in query_result] #obtain the number of the document from its name
    results = df3.iloc[lines_1,]   
    cosine_score=[cosinesimilarity_1[key] for key in cosinesimilarity_1.keys()] #list with all the results from the cosine similarity    
    results.insert(loc= 4, column = 'Score', value = cosine_score) #insert the values in the dataframe with the selected dataframes
    indexis_1 = results.index.tolist() #list with indexes of result dataframe
    scores_1 = results['Score'].tolist() #list with score values
    h_1 = [] 
    top_k_1 = []
    #loops using heap to order the scores of the documents from the higher to the lower
    for i in range(len(scores_1)):
        heappush(h_1, (-scores_1[i], indexis_1[i])) 
    top_k_1 = []
    if len(results) < 10:
        for i in range(len(results)):
            top_k_1.append(heappop(h_1))
    else:
        for i in range(10):
            top_k_1.append(heappop(h_1))
    top_k_doc_1 = []
    for i in range(len(top_k_1)):
        top_k_doc_1.append(top_k_1[i][1])
    #storing the documents ordered in dataframe and showing them    
    results_top_k_1 = results.loc[top_k_doc_1,:] 
    display(HTML(tabulate(results_top_k_1, headers= ['Title', 'Description','City','Url', 'Score'], showindex=False, tablefmt="html")))


