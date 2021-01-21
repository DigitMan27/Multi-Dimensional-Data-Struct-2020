'''

Author : Κωνσταντίνος Αδαμόπουλος
ΑΜ: 236270 (1043750)
Ετος: 7ο

'''

import random
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

from core.Voronoi2D import Voronoi2D


def generatePoints(numSeeds):
	'''
		Η συνάρτηση αυτή παράγει τυχαία 2D σημεία 
		το όρισμα numSeeds αφορά τόν αριθμό των σημείων .
	'''
	radius = 100
	seeds = radius * np.random.random((numSeeds, 2))
	return seeds
    

def loadGeoDataset1(size):
	'''
		Η συναρτηση αυτη φορτώνει την πολιτεια της Νεας Υορκης 
		και καποια σημεια ενδιαφέροντος και τα χρησιμοποιώ ωστε να αναπαράγω το δίαγραμμα
		Voronoi των σημείων αυτων . 

		Πηγες: 
			Το αρχείο της μεταβλητής gmap το πήρα απο :
			https://tapiquen-sig.jimdofree.com/english-version/free-downloads/united-states/
			
			Το αρχείο της μεταβλητής file το πήρα απο :
			https://www1.nyc.gov/site/doitt/residents/gis-2d-data.page

	'''
	file = "data/dataset1/Points Of Interest/geo_export_d771d7a5-ef72-43f8-8b2c-67a3549235c5.shp"
	gmap = "data/USA_States/USA_States.shp"
	points = gpd.read_file(file)
	points = points.to_crs({"init": "EPSG:4326"})
	city = gpd.read_file(gmap)
	city = city.to_crs(points.crs)
	city = city[city["STATE_NAME"] == "New York"]
	points = gpd.sjoin(points,city,how="left")
	points = points.dropna(subset=["index_right"])
	numOfPoints = points.shape[0]

	dataSize = points.shape[0]
	if dataSize > size:

		x = points.geometry.x[0:size]
		y = points.geometry.y[0:size]

		intrest_points_nparr = np.array([[i,j] for i,j in zip(x,y)])
		
		return intrest_points_nparr[0:size,:], city, size
	else:
		return [],[],[],[]


def loadGeoDataset2():
	'''
		Η συναρτηση αυτη φορτώνει την πρωτέυουσα που έχει η κάθε πολιτεία
		και τις πολιτείες της Αμερικής. 

		Πηγες: 
			Το αρχείο της μεταβλητής gmap το πήρα απο :
			https://tapiquen-sig.jimdofree.com/english-version/free-downloads/united-states/
			
			Το αρχείο της μεταβλητής file το πήρα απο :
			https://tapiquen-sig.jimdofree.com/english-version/free-downloads/united-states/

	'''
	file = "data/dataset2/USA_Capitals/USA_Capitals.shp"
	gmap = "data/USA_States/USA_States.shp"
	points = gpd.read_file(file)
	points = points.to_crs({"init": "EPSG:4326"})
	x = points.geometry.x
	y = points.geometry.y
	capital_points_nparr = np.array([[i,j] for i,j in zip(x,y)])

	states = gpd.read_file(gmap,header=None)
	states = states.to_crs(points.crs)
	
	return capital_points_nparr, states.geometry

if __name__=="__main__":
	
	# Παραγωγή διαγράμματος Voronoi τυχαίων σημείων
	'''
	points = generatePoints(100)
	vor = Voronoi2D(points)
	vor.start()
	vor.plotVoronoi()
	'''
	

	# Παραγωγή διαγράμματος Voronoi ενος συνόλου των σημείων ενδιαφέροντος που υπάρχουν στην Νεα Υορκη .
	'''
	points, city, totalSize = loadGeoDataset1(100)
	#print('Number of Points:',totalSize)
	
	
	if len(points)>0:
		vor = Voronoi2D(points)
		vor.start()
		vor.plotVoronoi(city=city)
	else:
		print('Εχείς εισάγει παραπάνω σημεια απο ότι περιέχονται στο Dataset.')
	'''
	
	# Παραγωγή διαγράμματος Voronoi των πρωτευουσών των πολιτειών της Αμερικής.
	
	points, states = loadGeoDataset2()
	vor = Voronoi2D(points)
	vor.start()
	vor.plotVoronoi(city=states)
	
	
