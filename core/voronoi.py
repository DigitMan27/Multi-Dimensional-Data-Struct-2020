# na dw gia to ti ginetai otan to circumcenter einai e3w apo to trigwno 
# na megalwsw tis boudary grammes twn regions
# region colors

from .triangulation import Delaunay, LineIsEqual
import matplotlib.pyplot as plt
from math import inf, sqrt
import numpy as np

def eDistx(x,y):
	return sqrt(pow((x-y),2))

def eDist(x,y):
	return sqrt(pow((x[0]-y[0]),2)+pow((x[1]-y[1]),2))

def removeDuplicates(lst): 
   # return [t for t in (set(tuple(i) for i in lst))] 
   data = []
   for x in lst:
    	for d in x:
    		data.append(d)

   #print(data)
   z = [t for t in (set(tuple(i) for i in data))]
   return z


def det(x,y):
	return x[0]*y[1] - x[1]*y[0]


def Voronoi1(points):
	result = Delaunay(points)
	print('------- Voronoi --------')
	print('Triangles:',result[0])
	voronoi_edges = []
	shared_edges= []

	for triangle in result[0]:
		center = triangle.circumcenter
		a = (det(center,triangle.c)-det(triangle.a,triangle.c))/det(triangle.b,triangle.c)
		b = (det(center,triangle.b)-det(triangle.a,triangle.b))/det(triangle.b,triangle.c)
		if(a>0 and b>0 and 1.0-a-b>0):
			pass
		else:
			cx = (triangle.a[0]+triangle.b[0]+triangle.c[0])/3
			cy = (triangle.a[1]+triangle.b[1]+triangle.c[1])/3
			center = (cx, cy)
			triangle.circumcenter = center
			print('Centroid Center',center)

	for triangle in result[0]:
		for edge in triangle.edges:
			isShared = False
			for other in result[0]:
				if other==triangle:
					continue
				for o_edge in other.edges:
					if LineIsEqual(edge,o_edge):
						tmp = [triangle.circumcenter,other.circumcenter]
						voronoi_edges.append(tmp)
						shared_edges.append(edge)
						isShared = True

	print('shared_edges:',shared_edges)
	for triangle in result[0]: # einai psilo etoimo alla uparxoun periptwseis pou den leitourgei swsta isws ftaei o tupos trigwnou otan ola den einai obtuse tote leitourgei
		center = triangle.circumcenter
		for edge in triangle.edges:
			if edge in shared_edges:
				print('shared_edge:',edge)
				continue
			#slope = (edge[1][1] - edge[0][1])/(edge[1][0]-edge[0][0])
			#k = -1/slope
			k = ((edge[1][1]-edge[0][1])*(center[0]-edge[0][0])-(edge[1][0]-edge[0][0])*(center[1]-edge[0][1]))/((edge[1][1]-edge[0][1])**2 + (edge[1][0]-edge[0][0])**2)
			#y = k*(10-center[0]) + center[1]
			x4 = center[0] - k*(edge[1][1]-edge[0][1])
			y4 = center[1] + k*(edge[1][0]-edge[0][0])
			if x4 > center[0]:
				xfinal = result[3][0]+10
				m = ((center[0]+x4)/2, (center[1]+y4)/2)
				s = (center[1]-y4)/(center[0]-x4)
				yfinal = s*(xfinal-m[0]) + m[1]

			elif x4< center[0]:
				xfinal = result[2][0]-10
				m = ((center[0]+x4)/2, (center[1]+y4)/2)
				s = (center[1]-y4)/(center[0]-x4)
				yfinal = s*(xfinal-m[0]) + m[1]
			if [center,(xfinal, yfinal)] not in voronoi_edges:
				voronoi_edges.append([center,(xfinal, yfinal)])
	print('V:',voronoi_edges)

	fig, ax = plt.subplots()
	xmin = result[2][0]-10
	xmax = result[3][0]+10
	ymin = result[2][1]-10
	ymax = result[3][1]+10
	plt.axis([xmin,xmax,ymin,ymax])
	x_vals = []
	y_vals = []
	for p1 in points:
		plt.plot(p1[0],p1[1],'ro')
	#plt.plot(center[0],center[1],'bx')
	for e in voronoi_edges:
		for l in e:
			x_vals.append(l[0])
			y_vals.append(l[1])
	print('-----------------')
	
	for i in range(0,len(x_vals)):
		plt.plot(x_vals[2*i:2*(i+1)],y_vals[2*i:2*(i+1)],'k')
	
	'''
	#triangles
	tx_vals = []
	ty_vals = []
	for t in result[0]:
		plt.plot(t.circumcenter[0],t.circumcenter[1],'kx')
		for e in t.edges:
			for l in e:
				tx_vals.append(l[0])
				ty_vals.append(l[1])
	plt.plot(tx_vals,ty_vals)
	'''
	plt.show()

