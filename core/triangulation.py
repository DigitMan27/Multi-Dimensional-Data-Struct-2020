'''
Υλοποίηση του Bowyer–Watson algorithm ωστε να 
υπολογίζω την Delaunay Triangulation για Ν σημεία στον 2D χώρο

'''

import matplotlib.pyplot as plt
from math import inf, sqrt
import numpy as np
from .structs import *


def getCircumcenter(a,b,c):
	ad = a.x*a.x + a.y*a.y
	bd = b.x*b.x + b.y*b.y
	cd = c.x*c.x + c.y*c.y
	D = 2*(a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y))
	centerX = 1 / D * (ad * (b.y - c.y) + bd * (c.y - a.y) + cd * (a.y - b.y))
	centerY = 1 / D * (ad * (c.x - b.x) + bd * (a.x - c.x) + cd * (b.x - a.x))
	return Point(centerX, centerY)

def eDist(x,y):
	return sqrt(pow((x.x-y.x),2)+pow((x.y-y.y),2))

def LineIsEqual(line1,line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False

def findMin(pos):
	x, y = inf, inf
	for p in pos:
		if x > p.x:
			x = p.x
		if y > p.y:
			y = p.y
	return Point(x, y)

def findMax(pos):
	x, y = 0, 0
	for p in pos:
		if x < p.x:
			x = p.x
		if y < p.y:
			y = p.y
	return Point(x, y)

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
		if (eDist(self.a,self.circumcenter) >= eDist(point,self.circumcenter)):
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

	sxmax = Point(maxPoint.x*2, minPoint.y/2) # b
	sxmin = Point(minPoint.x*(-2), minPoint.y/2) # a
	symax = Point((sxmin.x+sxmax.x)/2, maxPoint.y*2) # c
	#print('sxmax:',sxmax)
	#print('sxmin:',sxmin)
	#print('symax:',symax)
	super_t = Triangle(sxmin,sxmax,symax)

	triangles.append(super_t)

	for point in points:
		bad_triangles = []
		#print('T len:',len(triangles))
		for triangle in triangles:
			#print(triangle.circumcenter)
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
	
	return final

def show(lst,points):
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


