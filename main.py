#from voronoi import Voronoi
from core.voronoi import Voronoi1
import random as r
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt


def generatePoints(Num):
	points = []
	for i in range(0,Num):
		points.append((r.randint(10,60),r.randint(2,50)))
	return points


if __name__=="__main__":
	#dataPath = '..\\data\\athensroads.shp'
	#dims = 2
	#v = Voronoi(dataPath,dims)
	p = generatePoints(5)
	points = np.array(p)

	Voronoi1(p)
	vor = Voronoi(points)
	fig = voronoi_plot_2d(vor)
	plt.show()
	#points = [(39, 16), (40, 41), (18, 32), (20, 5)]
	#points = [(28, 7), (28, 47), (40, 41), (24, 33), (14, 17)]
	#points = [(27, 29), (12, 14), (28, 16), (31, 34), (19, 2)]
	#print('points: ',points)
	#Voronoi(points)

	#res = Delaunay(points)
	#print(res)
	#print('len: ',len(t))
	#for tr in t:
	#	print(tr.edges)
	#show(res[0],res[1])