
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import nltk
import csv
import io
import json
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import heapq


# In[10]:

#this function clean the input that the user gives
def query_creation(input_):
    stop_words = set(stopwords.words('english')) #we take the stopwords we have to delete
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()
    words = word_tokenize(input_)
    words_without_stop_words = ["" if word in stop_words else word for word in words] #we delete the stopwords
    new_words = " ".join(words_without_stop_words)
    b = tokenizer.tokenize(new_words)
    l_query = []
    #with a for loop we stem all the words in the input, and store them in a list
    for word in b:
        l_query.append(ps.stem(word))
    #here we transform the list in a string
    query = ' '.join(l_query)
    return [l_query, query]


# In[9]:

#this function creates my score
def score(request, results, avg_price_night, bedrooms_count):
    city = request[0]
    price_night = request[1]
    n_bedrooms = request[2]
    #inizialize a list in wich we will store all the scores we will calculate for each result of the query
    scores = []
    for i in range(len(results)):
        #inizialize the counter for the score in each for
        count = 0
        #if the city of the result is the same that the user has specified we add 1 to the counter
        if city == results.iloc[i,2]:
            count += 1
        #if the price of the result is the same of the price specified from the user we add 0.5             
        if price_night == avg_price_night[i]:
            count += 0.5
        #if is lower, but not lower of 20 dollarsm we give more points, so 0.7
        elif avg_price_night[i] < price_night and avg_price_night[i] > (price_night - 20):
            count += 0.7
        #if is lower even of 20 dollars we give one point
        elif avg_price_night[i] <= (price_night - 20):
            count += 1
        #if is greater of 20 dollars we just add 0.3 point, but we do not give any point if is greater than 20 dollars
        elif avg_price_night[i] > price_night and avg_price_night[i] < (price_night + 20):
            count += 0.3
        #if the number of bedrooms that the user specifies is equal to the result we add 1 point
        if n_bedrooms == bedrooms_count[i]:
            count += 1
        #if the number of bedrooms of the result is greater or lower of 1 we add 0.7 point
        elif n_bedrooms == (bedrooms_count[i]-1) or n_bedrooms == (bedrooms_count[i]+1):
            count += 0.7
        #if is greater or lower of 2 we add 0.5 points
        elif n_bedrooms == (bedrooms_count[i]-2) or n_bedrooms == (bedrooms_count[i]+2):
            count += 0.5
        scores.append(count)
    return scores


# In[11]:

# function that execute the last query
def query_results(l_query, df_score):
    #we store our vocabulary
    with open('vocabulary.tsv') as f:
        vocabulary_load = json.load(f)
    idx = []
    #we look for the index that corresponds to each word
    for word in l_query:
        idx.append(vocabulary_load[word])
    with open('inverted_index.tsv') as f:
        inv_indx = json.load(f)
    #we look for the index in the indexes file
    idx_results = [inv_indx[str(i)] for i in idx]
    #we select the documents that has all the indexes, so all the words
    query_result=set.intersection(*map(set, idx_results))
    lines = [int(i[2:])-1 for i in query_result]
    #we select the documents from the dataframe
    results = df_score.iloc[lines,]
    #with the for loop we transform the column of the prices in integers, saving them in a list, for the next steps
    avg_price_night = []
    for i in range(len(results)):
        try:
            price = results['average_rate_per_night'][i]
            price = price[1:]
            price = int(price)
        except:
            price = 0
        avg_price_night.append(price)
    #with the for loop we transform the column of the numbe of bedrooms in integers, saving them in a list, for the next steps
    bedrooms_count =[]
    for i in range(len(results)):
        if results.iloc[i,5] == 'Studio':
            bedrooms_count.append(1)
        else:
            bedrooms_count.append(int(results.iloc[i,5]))
    #we give three input to ask at the user to specify how much they want to pay, how many bedrooms they need, and in which city they want to stay
    price_night= int(input('Which price do you want to pay per night: '))
    n_bedrooms = int(input('How many bedrooms do you need: '))
    city = input('In which city do you want to go: ')
    request = [city, price_night, n_bedrooms]
    #we use our score function to calculate our new score
    ranking = score(request, results, avg_price_night, bedrooms_count)
    #we add to the dataframe the column with the score for each result of the query
    results.insert(loc= 6, column = 'Score', value = ranking)
    indexis = results.index.tolist()
    scores = results['Score'].tolist()
    #we transform our data in heap data
    h = []
    for i in range(len(scores)):
        heapq.heappush(h, (-scores[i], indexis[i]))
    #we take 10 results with the higher score
    top_k = []
    if len(results) < 10:
        for i in range(len(results)):
            top_k.append(heapq.heappop(h))
    else:
        for i in range(10):
            top_k.append(heapq.heappop(h))
    top_k_doc = []
    #we take just the numbers of the 10 lines we will have to select from the results
    for i in range(len(top_k)):
        top_k_doc.append(top_k[i][1])
    #we select the lines of the top 10 results
    results_top_k = results.loc[top_k_doc,:]
    return results_top_k

