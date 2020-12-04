'''
Υλοποίηση του Bowyer–Watson algorithm ωστε να 
υπολογίζω την Delaunay Triangulation για Ν σημεία στον 2D χώρο

'''

import matplotlib.pyplot as plt
from math import inf, sqrt
import numpy as np


def getCircumcenter(a,b,c):
	ad = a[0]*a[0] + a[1]*a[1]
	bd = b[0]*b[0] + b[1]*b[1]
	cd = c[0]*c[0] + c[1]*c[1]
	D = 2*(a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1]))
	centerX = 1 / D * (ad * (b[1] - c[1]) + bd * (c[1] - a[1]) + cd * (a[1] - b[1]))
	centerY = 1 / D * (ad * (c[0] - b[0]) + bd * (a[0] - c[0]) + cd * (b[0] - a[0]))
	return centerX, centerY

def eDist(x,y):
	return sqrt(pow((x[0]-y[0]),2)+pow((x[1]-y[1]),2))

def LineIsEqual(line1,line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False

def findMin(pos):
	x, y = inf, inf
	for t, k in pos:
		if x>t:
			x = t
		if y > k:
			y = k
	return x, y

def findMax(pos):
	x, y = 0, 0
	for t, k in pos:
		if x<t:
			x = t
		if y < k:
			y = k
	return x, y

class Triangle:
	def __init__(self,a,b,c):
		self.a = a
		self.b = b
		self.c = c
		self.edges = [[self.a, self.b],
					  [self.b,self.c],
					  [self.c,self.a]]
		self.circumcenter = getCircumcenter(a,b,c)

	def isPointInCircumcenter(self,point):
		if (eDist(self.a,self.circumcenter) > eDist(point,self.circumcenter)):
			return True
		return False

	def HasVertex(self,point):
		if (self.a==point) or (self.b==point) or (self.c==point):
			return True
		return False


def Delaunay(points):
	triangles = []
	final = []

	#print('points: ',points)
	minPoint = findMin(points)
	maxPoint = findMax(points)
	print('min:',minPoint)
	print('max:',maxPoint)

	sxmax = (maxPoint[0]*2, minPoint[1]/2) # b
	sxmin = (minPoint[0]*(-2), minPoint[1]/2) # a
	symax = ((sxmin[0]+sxmax[0])/2, maxPoint[1]*2) # c
	#print('sxmax:',sxmax)
	#print('sxmin:',sxmin)
	#print('symax:',symax)
	super_t = Triangle(sxmin,sxmax,symax)

	triangles.append(super_t)

	for point in points:
		bad_triangles = []
		#print('T len:',len(triangles))
		for triangle in triangles:
			if triangle.isPointInCircumcenter(point):
				bad_triangles.append(triangle)
		#print('bad:',len(bad_triangles))
		polygon = []
		for triangle in bad_triangles:
			for edge in triangle.edges:
				isShared = False
				for other in bad_triangles:
					if triangle == other:
						continue
					for o_edge in other.edges:
						if LineIsEqual(edge,o_edge):
							isShared = True
				if(isShared==False):
					polygon.append(edge)
		for triangle in bad_triangles:
			triangles.remove(triangle)
		for edge in polygon:
			new_triangle = Triangle(edge[0],edge[1],point)
			triangles.append(new_triangle)
	for triangle in triangles:
		if triangle.HasVertex(sxmax)==False and triangle.HasVertex(sxmin)==False and triangle.HasVertex(symax)==False:
			final.append(triangle)
	triangles = []
	print('Ccenter:',final[0].circumcenter)
	return (final, points)

def show(fig,lst,points):
	fig, ax = plt.subplots()
	plt.axis([-1,60+1,-1,60+1])
	x_vals = []
	y_vals = []
	for p1 in points:
		plt.plot(p1[0],p1[1],'ro')
	for t in lst:
		for e in t.edges:
			for l in e:
				x_vals.append(l[0])
				y_vals.append(l[1])
	plt.plot(x_vals,y_vals)
	plt.show()
	#print(x_vals)


