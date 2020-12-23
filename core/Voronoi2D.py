from .triangulation import Delaunay, LineIsEqual
import matplotlib.pyplot as plt
from math import inf, sqrt, floor, cos, pi, sin, isclose, atan
import numpy as np

class convexPoly:

	def __init__(self,p1,p2,p3,p4):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4

		self.bounds = [Line(self.p1,self.p2),Line(self.p2,self.p3),Line(self.p3,self.p4),Line(self.p4,self.p1)]

class Point:

	def __init__(self,x,y):
		self.x = x
		self.y = y

class Line:
	def __init__(self,start,end=None,isDone=False):
		self.start = start
		self.end = end
		self.isDone = isDone

	def isFinished(self,end):
		if self.isDone:
			return
		self.end = end
		self.isDone = True

class Voronoi2D:

	def __init__(self,points):

		self.output = []
		self.sites = []
		self.triangles = []
		self.voronoi_lines = []

		# bounds
		self.x0 = 0
		self.x1 = 0
		self.y0 = 0
		self.y1 = 0

		points.sort(key=lambda tup: tup[0])
		print(points)
		for pts in points:
			point = Point(pts[0],pts[1])
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

		self.sharedEdges = []

		self.poly = convexPoly(Point(self.x0,self.y0),Point(self.x0,self.y1),Point(self.x1,self.y1),Point(self.x1,self.y0))

		self.triangles = Delaunay(points)
		self.t = Delaunay(points)
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
			self.find_boundaries()
		elif len(self.triangles) >= 2:
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
				print(edge)
				isShared = False
				for other in self.triangles:
					if other == triangle:
						continue
					for o_edge in other.edges:
						if LineIsEqual(edge,o_edge) :# and not self.collinear(edge):
							c1 = Point(triangle.circumcenter[0],triangle.circumcenter[1])
							c2 = Point(other.circumcenter[0],other.circumcenter[1])
							self.voronoi_lines.append(Line(c1,c2,True))
							#triangle.edges.remove(edge)
							#other.edges.remove(o_edge)
							self.sharedEdges.append(edge)
							self.sharedEdges.append(o_edge)
							isShared = True
						#elif LineIsEqual(edge,o_edge) and self.collinear(edge):
						#	other.edges.remove(o_edge)
		#print(self.voronoi_lines)

	def find_boundaries(self):
		for triangle in self.triangles:
			flag = False
			tmp = None
			center = Point(triangle.circumcenter[0],triangle.circumcenter[1])
			for edge in triangle.edges:
				print(edge)
				if edge in self.sharedEdges:
					continue
				flag, tmp = isObtuse(triangle)
				print(flag,tmp)
				if flag:
					p = self.intersect(edge,center,True,tmp)
					if p is not None:
						self.voronoi_lines.append(Line(p,center))

				else:
					p = self.intersect(edge,center)
					if p is not None:
						self.voronoi_lines.append(Line(p,center))
					else:
						print('None')
				
		print(self.voronoi_lines,len(self.voronoi_lines))

	def point_side(self,edge,point):
		x0 = edge[0][0]
		y0 = edge[0][1]
		x1 = edge[1][0]
		y1 = edge[1][1]
		D = ((x1-x0)*(point.y-y0) - (y1-y0)*(point.x - x0))
		if D > 0:
			return 'p'
		elif D<0:
			return 'n'
		else:
			return None

	def dist(self,p0,p1):
		#return sqrt((p1.x-p0.x)**2 + (p1.y-p0.y)**2)
		return abs((p1.x-p0.x)+(p1.y-p0.y))

	def intersect(self,edge,center,isObtuse=False,hypot=None):
		x0 = edge[0][0]
		y0 = edge[0][1]
		x1 = edge[1][0]
		y1 = edge[1][1]
		if(x1-x0)==0:
			print('p x')
			#return None # inf slope -> symetric to y axis 
			m = (x0+x1)/2, (y1+y0)/2
			#if m[1] < 
			if m[0] < center.x:
				return Point(self.x0,center.y)
			else:
				return Point(self.x0,center.y)
		elif(y1-y0)==0:
			print('p y')
			m = (x0+x1)/2, (y1+y0)/2
			#if m[1] < 
			if m[1] < center.y:
				return Point(center.x,self.y0)
			else:
				return Point(center.x,self.y1)
		else:
			'''slope = (y1 - y0)/(x1 - x0)
			p_slope = -1/slope
			b = center.y - p_slope*center.x'''

			if isObtuse==False:
				print('No isObtuse')
				k = ((y1-y0)*(center.x-x0)-(x1-x0)*(center.y-y0))/((y1-y0)**2 + (x1-x0)**2)
				x4 = center.x - k*(y1-y0)
				y4 = center.y + k*(x1-x0)
				print(x4,y4)
				slope = (y4-center.y)/(x4-center.x)
				b = y4 - slope*x4
				x = pi + k
				s1 = 1/slope
				print(atan(x))
				if center.x > x4 and -1/slope < 0:
					py = s1*self.x0 + b
					return Point(self.x0,py)
				elif center.x > x4 and -1/slope > 0:
					py = s1*self.x0 + b
					return Point(self.x0,py)
				elif x4 > center.x and -1/slope < 0:
					py = s1*self.x1 + b
					return Point(self.x1,py)
				elif x4 > center.x and -1/slope > 0:
					py = s1*self.x1 + b
					return Point(self.x1,py)
			else:
				k = ((y1-y0)*(center.x-x0)-(x1-x0)*(center.y-y0))/((y1-y0)**2 + (x1-x0)**2)
				x4 = center.x - k*(y1-y0)
				y4 = center.y + k*(x1-x0)
				print(x4,y4)
				slope = (y4-center.y)/(x4-center.x)
				b = y4 - slope*x4
				x = pi + k
				s1 = 1/slope
				print(slope)
				if center.x > x4 and -1/slope < 0:
					py = s1*self.x1 + b
					return Point(x4,y4)
				elif center.x > x4 and -1/slope > 0:
					py = s1*self.x1 + b
					#return Point(self.x1,py)
					return Point(x4,y4)
				elif x4 > center.x and -1/slope < 0:
					py = s1*self.x0 + b
					#return Point(self.x0,py)
					return Point(x4,y4)
				elif x4 > center.x and -1/slope > 0:
					py = s1*self.x0 + b
					return Point(x4,y4)
					#return Point(self.x0,py)

	def collinear(self,e1):
		if e1[0][0]==e1[0][1] or e1[0][1] == e1[1][0]:
			return True
		return False
			
	def get_output(self):
		for o in self.voronoi_lines:
			p0 = o.start
			p1 = o.end
			print('[',(p0.x,p0.y),',',(p1.x,p1.y),']')

	def showVoronoi(self):
		fig, ax = plt.subplots()
		ax.set_ylim([self.y0,self.y1])
		ax.set_xlim([self.x0,self.x1])

		for triangle in self.triangles:
			plt.plot(triangle.circumcenter[0],triangle.circumcenter[1],'rx')
		#plt.plot(self.triangles[0].circumcenter,'kx')
		for point in self.sites:
			plt.plot(point.x,point.y,'ro')

		for line in self.poly.bounds:
			plt.plot((line.start.x,line.end.x),(line.start.y,line.end.y),'k')

		for line in self.voronoi_lines:
			plt.plot((line.start.x,line.end.x),(line.start.y,line.end.y),'k')

		
		for t in self.t:
			for edge in t.edges:
				plt.plot((edge[0][0],edge[1][0]),(edge[0][1],edge[1][1]),'y')
		

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

def isObtuse(triangle): # na dw ti paizei me ta amblugwnia kai na ftia3w ligo tis peirptwseis douleuoume me circumecenter twra oxi centroid kapou paei na doume ....
	print('triangle')
	print(triangle.edges)
	print('end')
	a = triangle.edges[2]
	b = triangle.edges[0]
	c = triangle.edges[1]

	da = sqrt((a[0][0]-a[1][0])**2+(a[0][1]-a[1][1])**2)
	db = sqrt((b[0][0]-b[1][0])**2+(b[0][1]-b[1][1])**2)
	dc = sqrt((c[0][0]-c[1][0])**2+(c[0][1]-c[1][1])**2)
	print('a',da)
	print('b',db)
	print('c',dc)
	slope1 = (a[1][1]-a[0][1])/(a[1][0]-a[0][0])
	#da**2 + db**2 < dc**2 and 
	if db > da and db > dc:
		hypot = b
	elif da > dc and da > db:
		hypot = a
	elif dc > da and dc > db:
		hypot = c

	if slope1 > 0:
		return True, hypot
	return False, None
	'''
	elif db > da and db > dc:
		if da**2 + dc**2 < db**2:
			return True, triangle.edges[0]
		return False, None
	elif da > dc and da > db:
		if dc**2 + db**2 < da**2:
			return True, triangle.edges[2]
		return False, None
	'''


