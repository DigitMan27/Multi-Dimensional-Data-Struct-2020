from core.Voronoi2D import Voronoi2D
import random
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd


def generatePoints(numSeeds,rad):
    radius = rad
    seeds = radius * np.random.random((numSeeds, 2))
    return seeds
    

def loadGeoData(file,gmap,size):
	#fig, ax = plt.subplots()
	#plt.axis('equal')
	points = gpd.read_file(file) #geometry[0].centroid.to_crs()
	points = points.to_crs({"init": "EPSG:4326"})
	city = gpd.read_file(gmap)
	city = city.to_crs(points.crs)
	city = city[city["STATE_NAME"] == "New York"]
	points = gpd.sjoin(points,city,how="left")
	points = points.dropna(subset=["index_right"])
	numOfPoints = points.shape[0]

	dataSize = points.shape[0]
	#print(dataSize)
	if dataSize > size:
		
		#city.plot(ax=ax,alpha=0.3, edgecolor="black", facecolor="white")
		#points.plot(ax=ax,alpha = 0.4, color="red", marker='$\\bigtriangledown$',)
		#plt.show()

		x = points.geometry.x[0:size]
		y = points.geometry.y[0:size]

		poly_centers = np.array([[i,j] for i,j in zip(x,y)])
		max_val_x = max(x)
		max_val_y = max(y)
		min_val_x = min(x)
		min_val_y = min(y)
		max_point = [max_val_x, max_val_y]
		min_point = [min_val_x,min_val_y]
		return poly_centers[0:size,:], city, numOfPoints
	else:
		return [],[],[],[]
	


if __name__=="__main__":
	#file = "data/TNC_Lands_Illinois.shp/TNC_Lands_Illinois.shp"
	file = "data/Points Of Interest/geo_export_d771d7a5-ef72-43f8-8b2c-67a3549235c5.shp"
	gmap = "data/USA_States/USA_States.shp"#USA_Cities_Towns/USA_Cities_Towns.shp" #cb_2018_us_state_5m/cb_2018_us_state_5m.shp"
	points, city, totalSize = loadGeoData(file,gmap,100)
	print('Number of Points:',totalSize)
	
	if len(points)>0:
		vor = Voronoi2D(points)
		vor.start()
		vor.plotVoronoi(city=city)
	else:
		print('Too much points!!!')
	
