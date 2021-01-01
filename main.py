#from voronoi import Voronoi
#from core.voronoi import Voronoi1
#from core.triangulation import Delaunay
from core.Voronoi2D import Voronoi2D
import random
import numpy as np
#from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt


def generatePoints(numSeeds):
    radius = 100
    seeds = radius * np.random.random((numSeeds, 2))
    return seeds


if __name__=="__main__":
	#seeds = np.random.random((10, 2))
	#print(seeds)
	#dataPath = '..\\data\\athensroads.shp'
	#dims = 2
	#v = Voronoi(dataPath,dims)
	#points = generatePoints(10)
	#points = np.array(p)
	#p = [(1,3),(1,1),(2,3),(3,2),(2,1)]
	#points = np.array(p)
	#vor = Voronoi(points)
	#fig = voronoi_plot_2d(vor)
	#plt.show()
	#points = [(39, 16), (40, 41), (18, 32), (20, 5)]
	#points = [(28, 7), (28, 47), (40, 41), (24, 33), (14, 17)]
	#points = [(27, 29), (12, 14), (28, 16), (31, 34), (19, 2)]
	#points = [(1,4), (3,5)]
	#points = [(12, 14), (31, 34), (19, 2), (28, 16),(3,5),(2,1),(40,6),(35,18),(14,17)]
	#points= generatePoints(8)
	#points = [(12, 18), (3, 5),(14,17)]
	#points = [(3, 3), (7, 30),(14,3)] #isoskeles peripou test
	#points = [(3,3),(14,3),(14,25)] #orthogwnio test
	#points = [(3,5),(7,6),(14,25)] # blabh paliiii
	#points = [(5,4),(2,4),(4,4),(10,4)]
	#points = [(2,1),(2,4),(2,7)]
	#points = [(1,2),(3,2),(1,7),(2,10),(5,7),(6,7),(9,12)]
	#points = [(2,10),(5,7),(6,7),(2,7)]
	#points = [(2,1),(5,1),(3,7),(10,13),(8,16),(20,25),(6,4),(14,30),(14,28),(5,16),(27,3),(33,6),(40,16)]
	#points = np.asarray([(5, 211), (16, 156), (23, 242), (36, 256), (48, 133), 
	#(90, 216), (208, 48), (292, 285)]) # big Error
	#v = Voronoi2D(points)
	#triangles = Delaunay(points)
	#for t in self.triangles:
	#				for edge in t.edges:
	#					plt.plot((edge[0].x,edge[1].x),(edge[0].y,edge[1].y),'slategrey')
	#v.start()
	#v.get_output()
	#v.showVoronoi(showTriangles=True,withColors=True) # showTriangles=True withColors=True
	points = generatePoints(10)
	print('points',points)
	
	vor = Voronoi2D(points)
	vor.start()
	vor.plotVoronoi()