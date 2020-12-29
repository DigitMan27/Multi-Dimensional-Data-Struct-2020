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