from voronoi import Voronoi

if __name=="__main__":
	dataPath = '..\\data\\athensroads.shp'
	dims = 2
	v = Voronoi(dataPath,dims)