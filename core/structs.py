from math import inf

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

	def toTuple(self):
		return (self.x, self.y)

class Line:
	def __init__(self,start,end=None,isDone=False,slope=None,intercept=None,center=None):
		self.start = start
		self.end = end
		self.isDone = isDone
		self.slope = slope
		self.intercept = intercept
		self.center = center

	def isFinished(self,end):
		if self.isDone:
			return
		self.end = end
		self.isDone = True

	def showCoords(self):
		return self.start.x, self.start.y, self.end.x, self.end.y

	def getList(self):
		return [self.start,self.end]

'''
	def lineMaxX(self):
		x = 0
		for px in [self.start.x, self.end.x]:
			if px > x:
				x = px

		return x

	def lineMinX(self):
		x = inf
		y = None
		for px in [self.start, self.end]:
			if px.x < x:
				x = px
				y = px.y

		return x

	def lineMinY(self):
		y = inf
		for py in [self.start.y, self.end.y]:
			if py < y:
				y = py

		return y

	def lineMaxY(self):
		y = 0
		for py in [self.start.y, self.end.y]:
			if py > y:
				y = py

		return y

'''
class Rect:
	def __init__(self,lines):
		self.lines = lines
		self.order = {key:[] for key in range(0,len(lines))}
		i=0
		for line in self.lines:
			self.order[i] = line
			i+=1

	
