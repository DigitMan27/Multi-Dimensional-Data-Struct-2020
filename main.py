#from voronoi import Voronoi
from core.voronoi import Voronoi
import random as r


def generatePoints(Num):
	points = []
	for i in range(0,Num):
		points.append((r.randint(10,40),r.randint(2,50)))
	return points


if __name__=="__main__":
	#dataPath = '..\\data\\athensroads.shp'
	#dims = 2
	#v = Voronoi(dataPath,dims)
	#points = generatePoints(5)
	#points = [(39, 16), (40, 41), (18, 32), (20, 5)]
	#points = [(28, 7), (28, 47), (40, 41), (24, 33), (14, 17)]
	points = [(27, 29), (12, 14), (28, 16), (31, 34), (19, 2)]
	print('points: ',points)
	Voronoi(points)

	#res = Delaunay(points)
	#print(res)
	#print('len: ',len(t))
	#for tr in t:
	#	print(tr.edges)
	#show(res[0],res[1])