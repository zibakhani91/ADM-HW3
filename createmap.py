
# coding: utf-8

# In[1]:

import pandas as pd
import folium
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt
import numpy as np


# In[2]:

def showmap(df1,coordinates,Distance):

	def haversine(lat1, lon1, lat2, lon2): # example: distance = haversine(lat1, lon1, lat2, lon2)
		
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) # convert decimal degrees to radians
		
		# haversine formula
		
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a))
		
		# Radius of earth in kilometers is 6371
		km = 6371 * c
		return km
	point1 = coordinates
	Distance_arr = [] 
	for i in range(0, len(df1)):
		point2 = (df1.iloc[i]['latitude'], df1.iloc[i]['longitude'])
		Distance_i = haversine(point1[0],point1[1],point2[0],point2[1])
		Distance_arr.append(Distance_i)
	f_map = folium.Map(
		location=coordinates,
		zoom_start=10,
		tiles='openstreetmap'
	)

	tooltip = 'Click me!'
	folium.Marker(point1, popup='<i>User Location</i>',
				  tooltip=tooltip,icon=folium.Icon(color='red', icon='info-sign')).add_to(f_map)
	n_nans_rel = 0
	n_abnbs = 0
	folium.Circle(
	location = point1,radius = Distance*1000
	).add_to(f_map)

	for i,Distance_i in enumerate(Distance_arr):
		
		if Distance_i <= Distance:
			
			point2 = [df1.iloc[i]['latitude'], df1.iloc[i]['longitude']]
			try:
				popup_msg = []
		  
				popup_msg = str('<i> Price/night: '+str(df1.iloc[i]['average_rate_per_night'])+'</i>')
				
				folium.Marker(point2, popup=popup_msg, tooltip=tooltip).add_to(f_map)
				n_abnbs +=1
			except:
			   
				n_nans_rel +=1

				
	print('Number of AirBNB''s: ' + str(n_abnbs))            
	print('Relative Number of NaN values for geographical Coordinates in the data subset: ' + str(n_nans_rel))
	f_map.fit_bounds(f_map.get_bounds())
	return f_map


# In[3]:

def getcor(df1):
    print("Enter Distance:")
    Distance = float(input())
    coordinates = []
    print("Enter coordinates:")
    for i in range(2):
        coord = float(input())
        coordinates.append(coord)
    f_map = showmap(df1,coordinates,Distance)
    return f_map

