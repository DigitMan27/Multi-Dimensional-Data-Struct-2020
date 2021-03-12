'''
Υλοποίηση του Bowyer–Watson incremental algorithm ωστε να 
υπολογίζω την Delaunay Triangulation για Ν σημεία στον 2D χώρο

'''

import matplotlib.pyplot as plt
import matplotlib
from math import inf, sqrt
import numpy as np

class Delaunay:
	def __init__(self,center=(0,0),radius=1000000):
		center = np.asarray(center)
		self.coords = [center+radius*np.array((-1,-1)),
					   center+radius*np.array((1,-1)),
					   center+radius*np.array((1,1)),
					   center+radius*np.array((-1,1))]

		self.triangles = {}
		self.circles = {}

		# counter clock wise τριγωνα
		# δύο υπερ-τρίγωνα 
		T1 = (0,1,3)
		T2 = (2,3,1)

		self.triangles[T1] = [T2,None,None]
		self.triangles[T2] = [T1,None,None]

		for triangle in self.triangles:
			self.circles[triangle] = self.circumcenter(triangle)

	def circumcenter(self,triangle):
		
		points = np.asarray([self.coords[v] for v in triangle]) #3x2 μητρωο σημεια των κορυφών του τριγωνου
		
		# 3x3 μητρωο εσωτερικου γινομένου μεταξυ των κορυφών η διαγωνιος δινει το μετρο και οι γραμμεσ,στηλεσ με i!=j δινουν τις σχεσεις καθετοτητας ή μη των κορυφων.
		points2 = np.dot(points,points.T) 
		
		A = np.bmat([[2*points2,[[1],
									[1],
									[1]]],
							[[[1,1,1,0]]]]) # μπλοκ μητρωο του μητρωου εσωτερικου γινομένου και των κορυφών
		
		b = np.hstack((np.sum(points*points,axis=1),[1])) # διανυσμα b που περιέχει το μέτρο και το 1 για την τελευταια προσθετη στήλη στο μοκ μητρωο
		
		x = np.linalg.solve(A,b) # υπολογισμος βαρυκεντρων συντεταγμένων λ .

		bcoords = x[:-1] 
		center = np.dot(bcoords,points) # μετατροπή βαρυκεντρων συντεταγμένων σε καρτεσιανές

		radius = np.linalg.norm(points[0] - center) # ακτινα 
		
		return (center, radius)

	def inCircle(self,triangle,p):
		center, radius = self.circles[triangle]
		return np.linalg.norm(center - p) <= radius

	def addPoint(self,point):

		point = np.asarray(point)
		idx = len(self.coords)

		self.coords.append(point)

		bad_triangles = []
		for triangle in self.triangles: # αν υπαρχουν σημεια μεσα στον κυκλο τοτε είναι "κακό" τρίγωνο
			if self.inCircle(triangle,point):
				bad_triangles.append(triangle)


		boundary = []
		triangle = bad_triangles[0] # "τυχαίο τρίγωνο"
		if bad_triangles[0]==None:
			triangle = bad_triangles[1]
		edge = 0 # "τυχαία" edge
		while True:
			triangle_opposite = self.triangles[triangle][edge] # γειτονικο τρίγωνο
			if triangle_opposite not in bad_triangles:
				boundary.append((triangle[(edge+1) % 3],triangle[(edge-1) % 3],triangle_opposite)) # ακμη και το τριγωνο στο οποιο "συνορευει- είναι κοινή"

				edge = (edge+1) % 3

				if boundary[0][0] == boundary[-1][1]:
					break

			else:
				# Μετακινηση στην επόμενη CCW ακμή στο απέναντι τρίγωνο 
				edge = (self.triangles[triangle_opposite].index(triangle)+1) % 3
				triangle = triangle_opposite # επόμενος γείτονας

		for triangle in bad_triangles:
			del self.triangles[triangle]
			del self.circles[triangle]

		new_triangles=[]
		for (e0, e1, triangle_opposite) in boundary:
			triangle = (idx, e0, e1) # νεο τρίγωνο με το σημείο p και τις κορυφες της ακμής (e0,e1) που συνορεύουν με το triangle_opposite
			self.circles[triangle] = self.circumcenter(triangle)
			self.triangles[triangle] = [triangle_opposite, None, None] # θέτω το απέναντι τρίγωνο γειτονα του τριγώνου
			# προσπαθω να θέσω γειτονα του απέναντι τριγωνου το νεο τρίγωνο
			if triangle_opposite:
				for i, neigh in enumerate(self.triangles[triangle_opposite]):
					if neigh:
						if e1 in neigh and e0 in neigh:
							self.triangles[triangle_opposite][i] = triangle

			new_triangles.append(triangle)


		# ενωνω τα τριγωνα μεταξυ τους (σχεση γειτνιασης)
		N = len(new_triangles)
		for i, triangle in enumerate(new_triangles):
			self.triangles[triangle][1] = new_triangles[(i+1) % N] # next
			self.triangles[triangle][2] = new_triangles[(i-1) % N] # prev

	def getInfo(self):

		return self.triangles, self.circles, self.coords

	def plotTriangles(self,points,triangles,radius):
		x, y = zip(*points)
		print(x)
		print(y)
		bounds = [min(x),max(x),min(y),max(y)]
		fig, ax = plt.subplots()
		ax.margins(0.1)
		ax.set_aspect('equal')
		plt.axis([bounds[0]-1, bounds[1]+1, bounds[2]-1, bounds[3]+1])
		ax.triplot(matplotlib.tri.Triangulation(x,y,triangles),'bo--')
		plt.show()

