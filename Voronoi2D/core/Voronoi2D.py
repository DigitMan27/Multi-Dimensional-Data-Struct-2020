import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

from core.triangulation import Delaunay


class Voronoi2D:
	def __init__(self,points):
		x, y = zip(*points)
		self.bounds = [min(x),max(x),min(y),max(y)]
		center = np.mean(points,axis=0)
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

		self.triangles, self.centers, self.coords = self.d.getInfo() # παιρνω τα τριγωνα, του κυκλους και στα σημεία απο την τριγωνοποίηση
		triangleUseVertex = {i:[] for i in range(len(self.coords))}
		triangleIndex = {}
		for tidx, (a,b,c) in enumerate(sorted(self.triangles)):
			self.voronoiPoints.append(self.centers[(a,b,c)][0])

			# Περιστρέφω το υπαρχων τρίγωνο CCW ανάλογα με την κορυφή αναφοράς/ με την κορυφή που θέλουμε να είναι τελευταία .
			# Αυτό γίνεται ωστε να έχω την σωστή σειρά αναφοράς των κορυφών του τριγώνου ανάλογα με το σημείο που χρησιμοποιείται εκείνη την στιγμή .
			# Καποια κορυφή μπορεί να είναι και σε παραπάνω απο 1 τρίγωνα -> αρα το σημείο θα είναι κοινό για τουλάχιστον 2 τρίγωνα .
			
			triangleUseVertex[a] += [(b,c,a)]
			triangleUseVertex[b] += [(c,a,b)]
			triangleUseVertex[c] += [(a,b,c)]

			# Εδώ ορίζονται τα παραπάνω τρίγωνα με ένα id το οποίο είναι το ίδιο με το id της του τριγώνου που χρησιμοποιύμε .
			# Οπότε με αυτο τον τρόπο δείχνω οτι τα παραπάνω τρίγωνα είναι ουσιαστικά τα ίδια αλλα περιστραμένα ανάλογα του σημείου με CCW φορά.
			triangleIndex[(a,b,c)] = tidx
			triangleIndex[(c,a,b)] = tidx
			triangleIndex[(b,c,a)] = tidx

		for point_idx in range(4,len(self.coords)):
			vertex = triangleUseVertex[point_idx][0][0]
			r = []
			for _ in range(len(triangleUseVertex[point_idx])):
				t = [t for t in triangleUseVertex[point_idx] if t[0]==vertex][0] # Τρίγωνο που ξεκινάει με την κορυφή v .
				r.append(triangleIndex[t]) # προσθέτω το id του τριγωνου που ξεκινά με την κορυφη v
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

		if city is not None:
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
