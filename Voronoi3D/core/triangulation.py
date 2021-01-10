import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# na dw ti paizei me ta boundaries kai gia to an tha paw me faces h akmes 

class Delaunay3D:
	def __init__(self,points):

		self.points = points

		X, Y, Z = zip(*points)

		# bres to max,min twn x,y,z
		min_max_x = [ min(X), max(X) ]
		min_max_y = [ min(Y), max(Y) ]
		min_max_z = [ min(Z), max(Z) ]

		# bres to eurws tis megisths apo thn elaxisth timh
		r_x = min_max_x[1] - min_max_x[0]
		r_y = min_max_y[1] - min_max_y[0]
		r_z = min_max_z[1] - min_max_z[0]

		# bres to max euros
		max_r = max([r_x, r_y, r_z])

		# bres to midpoint meta3u tou max kai min timwn
		mid = [ sum(min_max_x)/2, sum(min_max_y)/2, sum(min_max_z)/2]

		#print(min_max_x)

		# tetrahedron coords
		self.coords = [[ mid[0] - 2*max_r, mid[1] - max_r, mid[2] - max_r ],
						[ mid[0] + 2*max_r, mid[1] - max_r, mid[2] - max_r ],
						[ mid[0], mid[1] + 2*max_r, mid[2] - max_r ],
						[ mid[0], mid[1], mid[2] + 2*max_r]]

		self.triangles = {}
		self.circles = {}

		T1 = (0,1,2,3) # CCW triangle
		#T2 = (1,2,3)
		self.triangles[T1] = [None,None,None,None] #isws thelei 6 logw akmwn kai oxi 4(faces)

		for triangle in self.triangles:
			self.circles[triangle] = self.circumcenter(triangle)


	def circumcenter(self,triangle):
		points = np.asarray([self.coords[v] for v in triangle]) #4x3 array

		innerProductMat = np.dot(points,points.T)

		A = np.bmat([[2*innerProductMat,[[1],
									[1],
									[1],
									[1]]],
							[[[1,1,1,1,0]]]])

		b = np.hstack((np.sum(points*points,axis=1),[1]))

		x = np.linalg.solve(A,b)

		bcoords = x[:-1]

		center = np.dot(bcoords,points)

		radius = np.linalg.norm(points[0] - center)

		return center, radius

	def inCircle(self,triangle,p):
		center, radius = self.circles[triangle]
		return np.linalg.norm(center - p) <= radius

	def addPoint(self,point):

		p = np.asarray(point)

		idx = len(self.coords)

		self.coords.append(point)

		bad_triangles = []
		for triangle in self.triangles:
			if self.inCircle(triangle,point):
				bad_triangles.append(triangle)

		print(bad_triangles)
		boundary = []
		triangle = bad_triangles[0]
		edge = 0
		while True:
			triangle_opposite = self.triangles[triangle][edge]
			if triangle_opposite not in bad_triangles:
				boundary.append((triangle[(edge+1) % 4],triangle[(edge-2) % 4],triangle[(edge-1) % 4],triangle_opposite))

				edge = (edge+1) % 6

				if boundary[0][0] == boundary[-1][1]:
					break

			else:
				edge = (self.triangles[triangle_opposite].index(triangle)+1) % 4
				triangle = triangle_opposite

		for triangle in bad_triangles:
			del self.triangles[triangle]
			del self.circles[triangle]

		new_triangles=[]
		print('opposite:',boundary)
		for (e0, e1, e2, triangle_opposite) in boundary:
			#print('edge:',e0, e1, triangle_opposite)
			triangle = (idx, e0, e1, e2) # dimourgw neo trigwno me to shmeio p kai tis akrianes akmes
			self.circles[triangle] = self.circumcenter(triangle)
			self.triangles[triangle] = [triangle_opposite, None, None, None] # 8ese san geitona tou trigwnou p ftia3ame to apenanti trigwno
			# prospa8hse na 8eseis san geitona tou opposite triangle to neo trigwno
			if triangle_opposite:
				for i, neigh in enumerate(self.triangles[triangle_opposite]):
					if neigh:
						if e1 in neigh and e0 in neigh and e2 in neigh:
							self.triangles[triangle_opposite][i] = triangle

			new_triangles.append(triangle)
			#print('new',new_triangles)
			N = len(new_triangles)
			for i, triangle in enumerate(new_triangles):
				self.triangles[triangle][1] = new_triangles[(i+1)%N]
				self.triangles[triangle][2] = new_triangles[(i-1)%N]
				self.triangles[triangle][3] = new_triangles[(i-2)%N]

		#print(self.triangles)



	def plot3DTriangles(self):
		fig = plt.figure()
		ax = Axes3D(fig)
		x, y, z = zip(*self.coords)
		#px, py, pz = zip(*self.points)
		ax.plot3D(x,y,z,'ko')
		#ax.plot3D(px,py,pz,'ro')
		for triangle in self.triangles:
			l = []
			lines = {}
			size = len(self.coords)
			for t in triangle:
				l1 = t%size
				l2 = (t+1)%size
				l3=(t+2)%size
				lines[l1] = [l2,l3]
			
			for d in lines:
				for l in lines[d]:
					l = [self.coords[d]]+[self.coords[l]]
					x,y,z = zip(*l)
					ax.plot3D(x,y,z,'black')
			

		plt.show()




