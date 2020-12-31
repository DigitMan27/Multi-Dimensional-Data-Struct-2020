'''
Υλοποίηση του Bowyer–Watson algorithm ωστε να 
υπολογίζω την Delaunay Triangulation για Ν σημεία στον 2D χώρο

'''

import matplotlib.pyplot as plt
import matplotlib
from math import inf, sqrt
import numpy as np
from .structs import *

class Delaunay:
	def __init__(self,center=(0,0),radius=9999):
		center = np.asarray(center)
		self.coords = [center+radius*np.array((-1,-1)),
					   center+radius*np.array((1,-1)),
					   center+radius*np.array((1,1)),
					   center+radius*np.array((-1,1))]

		self.triangles = {}
		self.circles = {}

		# counter clock wise triangles 
		T1 = (0,1,3) 
		T2 = (2,3,1)

		self.triangles[T1] = [T2,None,None]
		self.triangles[T2] = [T1,None,None]

		for triangle in self.triangles:
			self.circles[triangle] = self.circumcenter(triangle)

	def circumcenter(self,triangle):
		#https://en.wikipedia.org/wiki/Barycentric_coordinate_system
		
		points = np.asarray([self.coords[v] for v in triangle]) #2x2 mat shmeia twn korufwn twn trigwnwn
		#print(points)
		points2 = np.dot(points,points.T) # 3x3 mat deixnei poia korufh einai ka8eth se poia kai poia korufh einai antiroph tespa deixnei sxeseis dieu8unseis
		#print('dot:',points2)
		A = np.bmat([[2 * points2,[[1],
									[1],
									[1]]],
							[[[1,1,1,0]]]]) # mplok mhtrww pou periexei tis "deiu8unseis twn korufwn meta3u tous" + tis korufes
		#print('A:',A)
		b = np.hstack((np.sum(points*points,axis=1),[1])) # dianusma b periexei to metro 
		#print(points*points)
		#print('b:',b)
		x = np.linalg.solve(A,b)
		#print('x:',x)
		bcoords = x[:-1] # barukentrikes suntetagmenes 
		#print('bc',bcoords)
		center = np.dot(bcoords,points) # kartesianes suntetagmenes apo tou baruketrikous suntelestes + shmeiea
		#print('center',center)

		radius = np.sum(np.square(points[0]-center))
		return (center, radius)

	def inCircle(self,triangle,p):
		center, radius = self.circles[triangle]
		return np.sum(np.square(center-p)) <= radius

	def addPoint(self,p):

		point = np.asarray(p)
		idx = len(self.coords)

		self.coords.append(p)

		bad_triangles = []
		for triangle in self.triangles:
			if self.inCircle(triangle,p):
				bad_triangles.append(triangle)

		boundary = []
		triangle = bad_triangles[0] # "random triangle"
		edge = 0 # "random" edge
		while True:
			triangle_opposite = self.triangles[triangle][edge]
			if triangle_opposite not in bad_triangles:
				boundary.append((triangle[(edge+1) % 3],triangle[(edge-1) % 3],triangle_opposite))

				edge = (edge+1) % 3

				if boundary[0][0] == boundary[-1][1]:
					break

			else:
				edge = (self.triangles[triangle_opposite].index(triangle)+1) % 3
				triangle = triangle_opposite

		for triangle in bad_triangles:
			del self.triangles[triangle]
			del self.circles[triangle]

		new_triangles=[]
		for (e0, e1, triangle_opposite) in boundary:
			triangle = (idx, e0, e1) # dimourgw neo trigwno me to shmeio p kai tis akrianes akmes
			self.circles[triangle] = self.circumcenter(triangle)
			self.triangles[triangle] = [triangle_opposite, None, None] # 8ese san geitona tou trigwnou p ftia3ame to apenanti trigwno
			# prospa8hse na 8eseis san geitona tou opposite triangle to neo trigwno
			if triangle_opposite:
				for i, neigh in enumerate(self.triangles[triangle_opposite]):
					if neigh:
						if e1 in neigh and e0 in neigh:
							self.triangles[triangle_opposite][i] = triangle

			new_triangles.append(triangle)


		# enwse ta nea trigwna meta3u tous
		N = len(new_triangles)
		for i, triangle in enumerate(new_triangles):
			self.triangles[triangle][1] = new_triangles[(i+1) % N] # next
			self.triangles[triangle][2] = new_triangles[(i-1) % N] # prev

	def getTriangles(self):

		triangles = []
		for (a,c,b) in self.triangles:
			if a>3 and b>3 and c>3:
				triangles.append((a-4,b-4,c-4))
		return triangles

	def plotTriangles(self,points,triangles,radius):
		x, y = zip(*points)
		print(x)
		print(y)
		bounds = [min(x),max(x),min(y),max(y)]
		fig, ax = plt.subplots()
		ax.margins(0.1)
		ax.set_aspect('equal')
		plt.axis([bounds[0]-1, bounds[1]+1, bounds[2]-1, bounds[3]+1])
		#plt.axis([-1,radius+1, -1, radius+1])
		ax.triplot(matplotlib.tri.Triangulation(x,y,triangles),'bo--')
		plt.show()

