import random
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
#import geopandas as gpd
#import pandas as pd

from core.triangulation import *

def generatePoints(numSeeds,rad):
    radius = rad
    seeds = radius * np.random.random((numSeeds, 3))
    return seeds


def plot3Dpoints(points):
	fig = plt.figure()
	ax = Axes3D(fig)
	x, y, z = zip(*points)
	#print(x,y,z)
	ax.plot3D(x,y,z,'ko')
	plt.show()


if __name__=="__main__":

	points = generatePoints(5,100)
	
	d = Delaunay3D(points)

	for p in points:
		d.addPoint(p)
		
	#print(d.coords)
	#d.plot3DTriangles()