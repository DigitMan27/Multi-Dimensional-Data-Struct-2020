import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from math import inf, sqrt, floor, cos, pi, sin, isclose, atan
import numpy as np
import random

from core.triangulation import Delaunay


class Voronoi2D:
	def __init__(self,points):
		x, y = zip(*points)
		self.bounds = [min(x),max(x),min(y),max(y)]
		#print(self.bounds)
		center = np.mean(points,axis=0)
		#print('center',center)
		self.d = Delaunay(center)
		self.triangles = []
		self.points = points
		self.voronoiPoints = []
		self.centers = []
		self.voronoiRegions = {}
		self.coords = []

	def start(self):
		for point in self.points:
			self.d.addPoint(point)

		self.triangles, self.centers, self.coords = self.d.getInfo()
		triangleUseVertex = {i:[] for i in range(len(self.coords))}
		triangleIndex = {}
		for tidx, (a,b,c) in enumerate(sorted(self.triangles)):
			self.voronoiPoints.append(self.centers[(a,b,c)][0])

			# peristofh tou uparxontos trigwnoun CCW analoga me tin korufh anaforas/me tin korufh p theloume na einai teleutaia
			# auto ginetai wste na exw tin swsth seira anaforas twn korufwn tou trigwnou analoga me to shmeio pou xrhsimopoieitai ekeinh thn stigmh
			# kapoia korufh mporei n einai kai se parapanw apo 1 => ara to shmeio tha einai koino gia 2 + trigwna
			triangleUseVertex[a] += [(b,c,a)]
			triangleUseVertex[b] += [(c,a,b)]
			triangleUseVertex[c] += [(a,b,c)]

			# edw orizontai ta parapanw trigwna me ena id to opoio einai to idio me to id ths emfaniseis tou kuriou trigwnou
			#opote auto shmainei oti ta parapanw trigwna einai ousiatika to trigwno me to sugkekrimeno id aplws apo allh optikh gwnia pou einai analogh tou shmeiou
			triangleIndex[(a,b,c)] = tidx
			triangleIndex[(c,a,b)] = tidx
			triangleIndex[(b,c,a)] = tidx

		for point_idx in range(4,len(self.coords)):
			vertex = triangleUseVertex[point_idx][0][0]
			r = []
			for _ in range(len(triangleUseVertex[point_idx])):
				t = [t for t in triangleUseVertex[point_idx] if t[0]==vertex][0] # trigwno pou 3ekinaei me thn v 
				r.append(triangleIndex[t]) # pros8etw to id tou trigwnou sthn perioxh
				vertex = t[1]
			self.voronoiRegions[point_idx-4] = r

		return self.voronoiPoints, self.voronoiRegions


	def plotVoronoi(self,fill=True,city=None):
		
		fig, ax = plt.subplots()
		ax.margins(0.1)
		ax.set_aspect('equal')
		plt.axis([self.bounds[0]-1, self.bounds[1]+1, self.bounds[2]-1, self.bounds[3]+1])
		if city is None:
			if not fill:
				for point in self.points:
					plt.plot(point[0],point[1],'rx')
				for region in self.voronoiRegions:
					poly = [self.voronoiPoints[i] for i in self.voronoiRegions[region]]
					plt.plot(*zip(*poly),color='black')

			else:
				for point in self.points:
					plt.plot(point[0],point[1],'kx')

				for region in self.voronoiRegions:
					poly = [self.voronoiPoints[i] for i in self.voronoiRegions[region]]
					plt.fill(*zip(*poly),alpha=0.5)
		else:
			if not fill:
				for point in self.points:
					plt.plot(point[0],point[1],'rx')

				for region in self.voronoiRegions:
					poly = [self.voronoiPoints[i] for i in self.voronoiRegions[region]]
					plt.plot(*zip(*poly),color='black')

				city.plot(ax=ax,alpha=0.3, edgecolor="black", facecolor="white")
			else:
				for point in self.points:
					plt.plot(point[0],point[1],'kx')

				for region in self.voronoiRegions:
					poly = [self.voronoiPoints[i] for i in self.voronoiRegions[region]]
					plt.fill(*zip(*poly),alpha=0.5)

				city.plot(ax=ax,alpha=0.6, edgecolor="black", facecolor="white")

		plt.show()
