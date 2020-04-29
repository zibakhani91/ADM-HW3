# Adm-Homework-3-group-26

# Find the perfect place to stay in Texas

The proposed scripts allow to use different search engines that given as input a query, return the entries of the accomodations that match the query. In order to do so, first the data is preprocessed. The first search engine return all the entries with the words in the query. The second search engine implemented apart from providing the entries with the words in the query, ranks the results regarding the cosine similarity using the tfIDf of the documents and query.  Afterwards, it is implemented another search engine with a new score that allows to take into consideration more features of the data. Finally, it is proposed a visualization with Folium where it is shown in the map, given a certain coordinates and radius, all the houses that are contained in a circle of that radius whose center is the coordinates provided. Besides, in the map it is also shown the price of each accomodation inside the radius.

## Data to analyse

The used data for the project was downloaded from the [Kaggle](https://www.kaggle.com/PromptCloudHQ/airbnb-property-data-from-texas) website. This data about Airbnb was extracted by PromptCloud's Data-as-a-Service solution for the Texas state of the USA. The dataset have information about the average rate per night, the number of bedrooms, the city, the date of listing, description of the place, latitude and longitude coordinates, title and url of about 18250 accomodation in Texas.



## Script descriptions

* `preprocessing.py`: Defines functions that allow to preprocess the downloaded text.

* `voc_ii_creation.py`: The codes provides the functions neccesary to create a vocabulary, an inverted index and an inverted index with the TfIdf coefficient. The output of this functions are in the folder `Files`.

* `queries.py`: Contain functions to make a conjunctive query without score and a conjunctive query using the cosine similarity.

* `newquery.py`: Defines a funtion to make a query using a different score to the cosine similarity taking advantage of different features of the data from the previous queries.

* `createmap.py`:  The code provides the functions neccesary to create a map with a marker for the location that the user has specified and a circle with the radius with the distance that  the user introduced.


**Remark:** In some of the functions in the `.py` scripts, it is necessary to change the name of the folder from where the files are read or in which one it is written for the name of a folder in the user computer.

## Jupyter Notebook

* `hm3.ipynb`: It is a `IPython notebook` where it is displayed how the classes and methods provided were used. 

**Remarks:**
 
 * Due to the fact that interactive plots are present, it is possible to read the Notebook correctly using this [link] (http://nbviewer.jupyter.org/github/Ilaria27/Adm-Homework-3-group-26/blob/master/Homework_3.ipynb).
 
 * Whether you are interested in running all the cells do that, otherwise, if you want just run the analysis, in the folder `files` you find all the data used in the further analysis that will make everthing faster. For the tidiness of the notebook the functions used in the script are strored in the `.py` scripts.

## References

* J. Leskovec, A. Rajaraman, and J. Ullman, "Mining of Massive Datasets," Cambridge University Press 

* C. D. Manning, P. Raghavan and H. Schütze, "Introduction to Information Retrieval," Cambridge University Press

