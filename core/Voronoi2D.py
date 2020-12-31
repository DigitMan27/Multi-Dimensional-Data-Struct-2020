from .triangulation import Delaunay, LineIsEqual, findMin, findMax
from .structs import *
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from math import inf, sqrt, floor, cos, pi, sin, isclose, atan
import numpy as np
import random


'''
exw fiat3ei ena dict wste na blepw se poia points antistoixoun poies grammes etsi isws na mporesw meta na xrwmatisw tis perioxes
na dw mhpws xreiastei na bgalw kapoia pragmata oso anafora tis listes pou apo8ukeuoun tis grammes
'''

class Voronoi2D:

	def __init__(self,points):

		self.output = []
		self.sites = []
		self.triangles = []
		self.voronoi_lines = []
		self.rects = []

		# bounds
		self.x0 = 0
		self.x1 = 0
		self.y0 = 0
		self.y1 = 0

		points.sort(key=lambda tup: tup[0])
		self.point_edges = {}
		self.boundary_edges = {}
		print(points)
		for pts in points:
			point = Point(pts[0],pts[1])
			self.point_edges[point] = []
			self.boundary_edges[point] = []
			self.sites.append(point)

			if point.x < self.x0:
				self.x0 = point.x
			if point.y < self.y0:
				self.y0 = point.y
			if point.x > self.x1:
				self.x1 = point.x
			if point.y > self.y1:
				self.y1 = point.y

		dx = (self.x1 - self.x0 + 1 )/5.0
		dy = (self.y1 - self.y0 + 1 )/5.0
		self.x0 -= dx
		self.x1 += dx
		self.y0 -= dy
		self.y1 += dy

		self.sharedEdges = {}

		self.poly = convexPoly(Point(self.x0,self.y0),Point(self.x0,self.y1),Point(self.x1,self.y1),Point(self.x1,self.y0))

		self.triangles = Delaunay(self.sites)

		#print(point_edges)
		'''
		flag = False
		edges = None
		for triangle in self.triangles:
			flag, edges = isObtuse(triangle)
			if flag:
				#self.triangles.remove(triangle)
				triangle.center = ((edges[0][0]+edges[1][0])/2, (edges[1][0]+edges[1][1])/2)
		'''

		'''
		print('edges')
		for triangle in self.triangles:
			if isObtuse(triangle):
				self.triangles.remove(triangle)

		for triangle in self.t:
			if isObtuse(triangle):
				self.t.remove(triangle)
		
		for triangle in self.triangles:
			#if not inside(triangle):
			cx = (triangle.a[0]+triangle.b[0]+triangle.c[0])/3
			cy = (triangle.a[1]+triangle.b[1]+triangle.c[1])/3
			center = (cx, cy)
			triangle.circumcenter = center
		'''


	def start(self):

		if len(self.triangles) == 1:
			for triangle in self.triangles:
				self.sharedEdges[triangle] = []
			self.find_boundaries()
		elif len(self.triangles) >= 2:
			for triangle in self.triangles:
				self.sharedEdges[triangle] = []
			self.find_cells()
			self.find_boundaries()
		elif len(self.triangles)==0:

			print('No triangles->collinear points aprox')
			visited = []
			#self.points.sort(key=lambda tup: tup[0])
			for point in self.sites:
				for p in self.sites:
					if point == p or p in visited:
						continue
					else:
						visited.append(point)
						if point.x == p.x :
							print('xxxxxx')
							m = (point.y + p.y)/2
							tmp = Point(point.x,m)
							self.voronoi_lines.append(Line(Point(self.x0,m),tmp))
							self.voronoi_lines.append(Line(Point(self.x1,m),tmp))
							break
						elif point.y == p.y:
							print('yyyyyy')
							m = (point.x + p.x)/2
							tmp = Point(m,point.y)
							self.voronoi_lines.append(Line(Point(m,self.y0),tmp))
							self.voronoi_lines.append(Line(Point(m,self.y1),tmp))
							break


	def find_cells(self):
		for triangle in self.triangles:
			for edge in triangle.edges:
				#print(edge)
				isShared = False
				for other in self.triangles:
					if other == triangle:
						continue
					#self.sharedEdges[other] = []
					for o_edge in other.edges:
						if LineIsEqual(edge,o_edge) :# and not self.collinear(edge):
							c1 = triangle.circumcenter
							c2 = other.circumcenter
							line = Line(c1,c2,True)
							self.point_edges[edge[0]].append(line)
							self.point_edges[edge[1]].append(line)
							self.voronoi_lines.append(line)
							triangle.edges.remove(edge) # ta diagrafw gia na apofugw to na exw 2 akmes ides aplws me antistrofa shmeia
							other.edges.remove(o_edge)
							self.sharedEdges[triangle].append(edge)
							self.sharedEdges[other].append(o_edge)
							isShared = True
						#elif LineIsEqual(edge,o_edge) and self.collinear(edge):
						#	other.edges.remove(o_edge)
		#print(self.voronoi_lines)

	def find_boundaries(self):
		for triangle in self.triangles:
			flag = False
			center = triangle.circumcenter
			flag = self.isObtuse(triangle)
			if flag: # center IN
				for edge in triangle.edges:
					if edge in self.sharedEdges[triangle]: # den polu xreiazetai edw twra afou ta diagrafw pio panw
						continue
					p, slope, b = self.intersect(edge,center)
					if p is not None:
						line = Line(p,center,True,slope,b,center)
						self.voronoi_lines.append(line)
						self.boundary_edges[edge[0]].append(line)
						self.boundary_edges[edge[1]].append(line)
					else:
						print('None')
			else:
				for edge in triangle.edges:
					if edge in self.sharedEdges[triangle]:
						continue
					print(edge)
					isHypot = self.isHypot(edge,triangle)
					print("HYPOT",isHypot)
					p, slope, b = self.intersect(edge,center,True,isHypot)
					if p is not None:
						line = Line(p,center,True,slope,b,center)
						self.voronoi_lines.append(line)
						self.boundary_edges[edge[0]].append(line)
						self.boundary_edges[edge[1]].append(line)
				
		print(self.voronoi_lines,len(self.voronoi_lines))

	def isObtuse(self,triangle):

		center = triangle.circumcenter
		triangleArea = self.isInside(triangle.a,triangle.b,triangle.c)
		#print('Area:',triangleArea)
		triangleArea1 = self.isInside(center,triangle.b,triangle.c)
		#print('Area1:',triangleArea1)
		triangleArea2 = self.isInside(triangle.a,center,triangle.c)
		#print('Area2:',triangleArea2)
		triangleArea3 = self.isInside(triangle.a,triangle.b,center)
		#print('Area3:',triangleArea3)
		if isclose(triangleArea,(triangleArea1+triangleArea2+triangleArea3)):
			print("IN")
			return True # inside
		return False # not 

	def isHypot(self,edge,triangle):
		flags = [False]*2
		i=0
		if len(self.sharedEdges[triangle]) > 0: # an uparxoun koines akmes tote epeidh tis diagrafw apo ta trigwna gia logous(des panw) meta enonwn tis listes wste na exw ousiastika olo to trigwno pali
			edgesList = triangle.edges + self.sharedEdges[triangle]
		else:
			edgesList = triangle.edges
		for o_edge in edgesList:
			if edge == o_edge:
				continue
			else:
				if self.dist(edge[0],edge[1],mode='euclidian') > self.dist(o_edge[0],o_edge[1],mode='euclidian'):
					print(self.dist(edge[0],edge[1],mode='euclidian'),'>',self.dist(o_edge[0],o_edge[1],mode='euclidian'))
					flags[i] = True
					i+=1
				else:
					return False
		if flags[0] and flags[1]:
			return True
		return False

		

	def isInside(self,p1,p2,p3):
		triangleArea = (p1.x*(p2.y-p3.y)+p2.x*(p3.y-p1.y)+p3.x*(p1.y-p2.y))/2.0
		return abs(triangleArea)

	def dist(self,p0,p1,mode='abs'):
		if mode=='abs':
			return abs((p1.x-p0.x)+(p1.y-p0.y))
		elif mode == 'euclidian':
			return sqrt((p1.x-p0.x)**2 + (p1.y-p0.y)**2)

	def intersect(self,edge,center,isObtuse=False,isHypot=False):
		x0 = edge[0].x
		y0 = edge[0].y
		x1 = edge[1].x
		y1 = edge[1].y
		if(x1-x0)==0:
			print('p x')
			#return None # inf slope -> symetric to y axis 
			m = (x0+x1)/2, (y1+y0)/2
			#if m[1] < 
			if m[0] < center.x:
				return Point(self.x0,center.y), 0.0, center.y
			else:
				return Point(self.x0,center.y), 0.0, center.y
		elif(y1-y0)==0:
			print('p y')
			m = (x0+x1)/2, (y1+y0)/2
			#if m[1] < 
			if m[1] < center.y:
				return Point(center.x,self.y0), None, self.y0
			else:
				return Point(center.x,self.y1), None, self.y1
		else:

			if isObtuse==False: # na dw ligo thn ka8etothta twn grammwn
				print('No Obtuse')
				k = ((y1-y0)*(center.x-x0)-(x1-x0)*(center.y-y0))/((y1-y0)**2 + (x1-x0)**2)
				x4 = center.x - k*(y1-y0)
				y4 = center.y + k*(x1-x0)
				#print(x4,y4)
				slope = (y4-center.y)/(x4-center.x) # elenxos gia otan to x4/y4 einai iso me to center
				b = center.y - slope*center.x
				s1 = slope
				#print(atan(x))
				if center.x > x4 and -1/slope < 0:
					py = s1*self.x0 + b
					return Point(self.x0,py), slope, b
				elif center.x > x4 and -1/slope > 0:
					py = s1*self.x0 + b
					return Point(self.x0,py), slope, b
				elif x4 > center.x and -1/slope < 0:
					py = s1*self.x1 + b
					return Point(self.x1,py), slope, b
				elif x4 > center.x and -1/slope > 0:
					py = s1*self.x1 + b
					return Point(self.x1,py), slope, b
			else:
				k = ((y1-y0)*(center.x-x0)-(x1-x0)*(center.y-y0))/((y1-y0)**2 + (x1-x0)**2)
				x4 = center.x - k*(y1-y0)
				y4 = center.y + k*(x1-x0)
				#print(x4,y4)
				slope = (y4-center.y)/(x4-center.x)
				b = center.y - slope*center.x
				s1 = slope
				#print(slope)
				if center.x > x4 and -1/slope < 0:
					if isHypot:
						py = s1*self.x1 + b
						return Point(self.x1,py), slope, b
					else:
						py = s1*self.x0 + b
						return Point(self.x0,py), slope, b
				elif center.x > x4 and -1/slope > 0:
					if isHypot:
						py = s1*self.x1 + b
						return Point(self.x1,py), slope, b
					else:
						py = s1*self.x0 + b
						return Point(self.x0,py), slope, b
					#return Point(x4,y4)
				elif x4 > center.x and -1/slope < 0: # na balw kai edw tin periptwsh me thn hypot
					if isHypot:
						py = s1*self.x1 + b
						return Point(self.x1,py), slope, b
					else:
						py = s1*self.x1 + b
						return Point(self.x1,py), slope, b
					#return Point(x4,y4)
				elif x4 > center.x and -1/slope > 0:
					if isHypot:
						py = s1*self.x0 + b
						return Point(self.x0,py), slope, b
					else:
						py = s1*self.x1 + b
						return Point(self.x1,py), slope, b

	def collinear(self,e1):
		if e1[0][0]==e1[0][1] or e1[0][1] == e1[1][0]:
			return True
		return False
			
	def get_output(self):
		for o in self.voronoi_lines:
			p0 = o.start
			p1 = o.end
			print('[',(p0.x,p0.y),',',(p1.x,p1.y),']')

	def colorGeneratorHex(self):
		num_of_colors = len(self.sites)
		pointColor = {}
		for point in self.sites:
			pointColor[point] = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
		return pointColor


	def generateRects(self):
		for point in self.sites:
			lines = []
			print('Point:',point.x,point.y)
			#print('color',colors[point])
			print('No.Lines:',len(self.boundary_edges[point]))
			for line in self.boundary_edges[point]:
				minP = findMin(line.getList())
				maxP = findMax(line.getList())
				lines.append(line)
				#print('line',minX,maxX,line.slope)
				#print('Min:',minX)
				#print('Max:',maxX)
				#A = np.linspace(minX,maxX)
				if minP.x <= self.x0:
					print('1')
					if line.center.y > point.y:
						print('10')
						y = self.y0
						p = Point(minP.x,y)
						line = Line(p,line.start)
						lines.append(line)
					elif point.y >= line.center.y:
						print('11')
						y = self.y1
						p = Point(minP.x,y)
						line = Line(p,line.start)
						lines.append(line)
				elif minP.y <= self.y0:
					print('2')
					if line.center.x > point.x:
						print('20')
						x = self.x0
						p = Point(x,minP.y)
						line = Line(p,line.start)
						lines.append(line)
					elif line.center.x < point.x:
						print('21')
						x = self.x1
						p = Point(x,minP.y)
						line = Line(p,line.start)
						lines.append(line)
				elif maxP.y >= self.y1:
					print('3')
					if line.center.x < point.x:
						print('31')
						x = self.x1
						p = Point(x,maxP.y)
						line = Line(p,line.start)
						lines.append(line)
					elif line.center.x > point.x:
						print('32')
						x = self.x0
						p = Point(x,maxP.y)
						line = Line(p,line.start)
						lines.append(line)
				elif maxP.x >= self.x1:
					print('4')
					if line.center.y < point.y:
						print('41')
						y = self.y1
						p = Point(maxP.x,y)
						line = Line(p,line.start)
						lines.append(line)
					elif line.center.y > point.y:
						print('42')
						y = self.y0
						p = Point(maxP.x,y)
						line = Line(p,line.start)
						lines.append(line)
			self.rects.append(Rect(lines))


	def showVoronoi(self,withColors=False,showTriangles=False):
		fig, ax = plt.subplots()
		ax.set_ylim([self.y0,self.y1])
		ax.set_xlim([self.x0,self.x1])

		if withColors==False:

			for triangle in self.triangles:
				plt.plot(triangle.circumcenter.x,triangle.circumcenter.y,'rx')
			
			for point in self.sites:
				plt.plot(point.x,point.y,'ro')

			for line in self.poly.bounds:
				plt.plot((line.start.x,line.end.x),(line.start.y,line.end.y),'k')

			for line in self.voronoi_lines:
				plt.plot((line.start.x,line.end.x),(line.start.y,line.end.y),'k')

			if showTriangles==True:
				for t in self.triangles:
					for edge in t.edges:
						plt.plot((edge[0][0],edge[1][0]),(edge[0][1],edge[1][1]),'slategrey')

				for edge in self.sharedEdges:
					plt.plot((edge[0].x,edge[1].x),(edge[0].y,edge[1].y),'slategrey')
		else:
			colors = self.colorGeneratorHex()
			colors = np.asarray(colors)
			#print('colors:',colors)
			for point in self.sites:
				plt.plot(point.x,point.y,'ko')

			for line in self.poly.bounds:
				plt.plot((line.start.x,line.end.x),(line.start.y,line.end.y),'k')

			for line in self.voronoi_lines:
				plt.plot((line.start.x,line.end.x),(line.start.y,line.end.y),'k')

			# for boundary points first
			#self.generateRects()
			'''
			patches = []
			for point in self.sites:
				l = len(self.boundary_edges[point])
				vertices = []
				#vertices.shape = (l,l)
				for line in self.boundary_edges[point]:
					tmp = [line.start.x,line.start.y],[line.end.x,line.end.y]
					vertices.append(tmp)
					#vertices = np.append(vertices,[line.end.x,line.end.y])
				print('V:',np.asarray(vertices))
				print('V:',np.asarray(vertices).shape)
				vertices = np.asarray(vertices).reshape((4,2))
				print(vertices)
				print('V:',vertices.shape)
				poly = Polygon(vertices,True)
				patches.append(poly)

			print(patches[0].get_xy())

			p = PatchCollection(patches,cmap=matplotlib.cm.jet)
			p.set_array(colors)

			ax.add_collection(p)
			'''

			#print(self.rects)

			if showTriangles==True:
				for t in self.triangles:
					for edge in t.edges:
						plt.plot((edge[0].x,edge[1].x),(edge[0].y,edge[1].y),'slategrey')

				for edge in self.sharedEdges:
					plt.plot((edge[0].x,edge[1].x),(edge[0].y,edge[1].y),'slategrey')

			#print(self.point_edges)

		plt.show()



def det(x,y):
	return x[0]*y[1] - x[1]*y[0]

def inside(triangle):
	center = triangle.circumcenter
	a = (det(center,triangle.c)-det(triangle.a,triangle.c))/det(triangle.b,triangle.c)
	b = (det(center,triangle.b)-det(triangle.a,triangle.b))/det(triangle.b,triangle.c)
	if(a>0 and b>0 and 1.0-a-b>0):
		return True
	return False

'''
if line.slope !=None:
						y = line.intercept + line.slope*A
						if point.y < line.center.y:
							
							print('normal slope')
							plt.fill_between(A, y, color=colors[point])
						else:
							#print(y)
							#print(self.y1 + y)
							y_inv = self.y1 + y
							print('Not normal slope')
							plt.fill_between(A, y,y_inv,where=y_inv>y, color=colors[point])
					else:
						if point.y < line.center.y:
							print('normal')
							plt.fill_between(A, self.y0, color=colors[point])
						else:
							print('Not normal')
							plt.fill_between(A, self.y1, color=colors[point])
'''
