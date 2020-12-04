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


def Voronoi(points):
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
	for triangle in result[0]: # na brw to convex hull edges - shared edges kateu8hnsh tou x mesw tou x4><center[0]
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
			if [center,(x4, y4)] not in voronoi_edges:
				voronoi_edges.append([center,(x4, y4)])
	print('V:',voronoi_edges)
	#z = removeDuplicates(voronoi_edges)
	#print('z:',z)

	#if len(voronoi_edges) == 0:
	#	triangle = result[0][0]
	'''
	for triangle in result[0]:
		center = triangle.circumcenter
		for edge in triangle.edges:
			if edge in shared_edges:
				continue
			print(edge)
			k = ((edge[1][1]-edge[0][1])*(center[0]-edge[0][0])-(edge[1][0]-edge[0][0])*(center[1]-edge[0][1]))/((edge[1][1]-edge[0][1])**2 + (edge[1][0]-edge[0][0])**2)
			x4 = center[0] - k*(edge[1][1]-edge[0][1])
			y4 = center[1] + k*(edge[1][0]-edge[0][0])
			print(center[0],' ',center[1],'->',x4,' ',y4,'k',k)
			#print(center[0],' ',center[1],'->',5*x4,' ',5*y4)
			try:
				s1 = (edge[1][1]-edge[0][1])/(edge[1][0]-edge[0][0])
				s2 = (y4-center[1])/(x4-center[0])
			except ZeroDivisionError:
				continue
			#b = y4 - s2*x4
			#print('slopes mul:',s1*s2)
			voronoi_edges.append([center,(x4, y4)])
			#voronoi_edges.append(limit)
	for e in voronoi_edges:
		print(e)
	'''

	fig, ax = plt.subplots()
	plt.axis([-1,60+1,-1,60+1])
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
	#x2,y2 = zip(*sorted(zip(x_vals,y_vals),key=lambda x: x[0]))
	#print('x:',x2)
	#print('y:',y2)
	'''
	tmp = []
	p=0
	for i in range(0,len(x_vals)):
		#print(len(tmp))
		#print(x,y)
		if p==2:
			print(tmp[0])
			plt.plot(tmp[0][0],tmp[0][1],'ko')
			plt.plot(tmp[1][0],tmp[1][1],'ko')
			tmp = []
			p=0
			tmp.append((x_vals[i], y_vals[i]))
		else:
			tmp.append((x_vals[i], y_vals[i]))
		p+=1
	print(tmp)
	plt.plot(tmp[0][0],tmp[0][1],'k')
	plt.plot(tmp[1][0],tmp[1][1],'k')
	'''
	#plt.plot(x_vals,y_vals,'k')
	for i in range(0,len(x_vals)):
		plt.plot(x_vals[2*i:2*(i+1)],y_vals[2*i:2*(i+1)],'k')
	plt.plot((20,15),(22,40),'k')
	#print(len(x_vals))
	'''
	plt.plot(x_vals[0:2],y_vals[0:2])
	plt.plot(x_vals[2:4],y_vals[2:4])
	plt.plot(x_vals[4:6],y_vals[4:6])
	plt.plot(x_vals[6:8],y_vals[6:8])
	plt.plot(x_vals[8:10],y_vals[8:10])
	plt.plot(x_vals[10:12],y_vals[10:12])
	plt.plot(x_vals[12:14],y_vals[12:14])
	plt.plot(x_vals[14:16],y_vals[14:16])
	plt.plot(x_vals[16:18],y_vals[16:18])
	'''
	tx_vals = []
	ty_vals = []
	for t in result[0]:
		plt.plot(t.circumcenter[0],t.circumcenter[1],'kx')
		for e in t.edges:
			for l in e:
				tx_vals.append(l[0])
				ty_vals.append(l[1])
	plt.plot(tx_vals,ty_vals)
	plt.show()

