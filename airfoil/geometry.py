import sys
import salome
import operator
import numpy as np
import os

ExportPath=os.path.join(os.getcwd(),'')

salome.salome_init()
theStudy = salome.myStudy

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

def getCoord(Vertex, coord):
	coordDict = {'x': 0,
		     'y': 1,
		     'z': 2}
	return geompy.PointCoordinates(Vertex)[coordDict[coord]]

def getPointsFilter(listPoints, coord, comp, value, func=lambda x: 0,
						    coordF = 'x'):
	"""
	 Get the points satisfying 
			coord_i > value + func(coordFunc_i)
			coord_i < value + func(coordFunc_i)
	 > or < depending on the value of comp 
	(operator.gt or operator.lt)
	"""
	coordDict = {'x': 0,
		     'y': 1,
		     'z': 2}
	result = []
	for point in listPoints:
	    coordValue=geompy.PointCoordinates(point)[coordDict[coord]]
	    coordFunc=geompy.PointCoordinates(point)[coordDict[coordF]]
	    #print coordValue, func(coordFunc)
	    #print geompy.PointCoordinates(point)[0]
	    if comp(coordValue, value + func(coordFunc)):
		result.append(point)
	return result


def equidistance(wire, dist, side=True, extend=False):
	points = geompy.ExtractShapes(wire, 
			geompy.ShapeType["VERTEX"], False)
	offsetPoints = []
	if side:
		angle = 90
	else:
		angle = -90
        for i in range(0,len(points)-1):
		x1 = getCoord(points[i], 'x'); x2 = getCoord(points[i+1],'x')
		y1 = getCoord(points[i], 'y'); y2 = getCoord(points[i+1],'y')
		Vector = geompy.MakeVectorDXDYDZ(x2-x1, y2-y1, 0)
		pointZ = geompy.MakeVertexWithRef(points[i], 0,0,1)
		VectorAxis = geompy.MakeVector(points[i], pointZ)
		VectorPer = geompy.MakeRotation(Vector, VectorAxis,
					  np.radians(angle))
		offsetPoints.append(geompy.MakeTranslationVectorDistance(
					points[i], VectorPer, dist))
	
	offsetPoints.append(geompy.MakeTranslationVectorDistance(
					points[-1], VectorPer, dist))
	if extend:
		offsetPoints.append(geompy.MakeTranslationVectorDistance(
				offsetPoints[-1], Vector, dist))
		x1 = getCoord(points[0], 'x'); x2 = getCoord(points[1],'x')
		y1 = getCoord(points[0], 'y'); y2 = getCoord(points[1],'y')
		Vector = geompy.MakeVectorDXDYDZ(x2-x1, y2-y1, 0)
		offsetPoints = [geompy.MakeTranslationVectorDistance(
				offsetPoints[0], 
				Vector, -dist)]+offsetPoints
		
		
	return  geompy.MakePolyline(offsetPoints)


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
#geompy.addToStudy( O, 'O' )
#geompy.addToStudy( OX, 'OX' )
#geompy.addToStudy( OY, 'OY' )
#geompy.addToStudy( OZ, 'OZ' )

f = open('naca23012.dat', 'r')
data = f.readlines()[1:]
f.close()
pts = [map(float,line.split()) for line in data]

i = 0
splinePoints = []
for x in pts:
      splinePoints.append(geompy.MakeVertex(x[0], x[1], 0))
      #geompy.addToStudy(splinePoints[i], 'pt' + str(i))
      i+=1


spline = geompy.MakePolyline(splinePoints, False)
#geompy.addToStudy( spline, 'spline' )

cw = 914.4
ct = 0.20*cw
cl = cw - ct
R = 0.026*cw
angle=+45
dist = 10

Scale = geompy.MakeScaleTransform(spline, O, cw)

geomObj = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(cw-ct, cw/2)
sk.addSegmentRelative(0, -cw)
Sketch = sk.wire(geomObj)

Compound = geompy.MakeVertexOnLinesIntersection(Scale, Sketch)
Partition = geompy.MakePartition([Sketch], [Compound], [], [],
				 geompy.ShapeType["WIRE"], 0, [], 0)
[Edge_1,Edge_2,Edge_3] = geompy.ExtractShapes(Partition, geompy.ShapeType["EDGE"], True)
ArcCenter = geompy.MakeVertexOnCurve(Edge_2, 0.5)
ArcPoint = geompy.MakeVertexWithRef(ArcCenter, -R, 0, 0)

[Edge_1,Edge_2] = geompy.SubShapes(Scale, [105, 19])
closestPoints = []
Edges = [Edge_1, Edge_2]
for i in range(0,2):
	closestPoints.append(geompy.ClosestPoints(ArcCenter, Edges[i]))
	coords = closestPoints[i][1][3:]
	closestPoints[i] = geompy.MakeVertex(coords[0],
					     coords[1],
					     coords[2])
	#geompy.addToStudy( closestPoints[i], 'closestPoint_%d' % i)

if getCoord(closestPoints[0],'y') > getCoord(closestPoints[1],'y'):
	closestPointUp = closestPoints[0]
	closestPointDown = closestPoints[1]
else:
	closestPointUp = closestPoints[1]
	closestPointDown = closestPoints[0]

Partition_1 = geompy.MakePartition([Scale], 
				[closestPointUp, closestPointDown], 
				[], [], geompy.ShapeType["WIRE"], 0, [], 0)

[Vertex_3,Vertex_4] = geompy.SubShapes(Scale, [122, 3])
Line_1 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)

Arc_1 = geompy.MakeArc(closestPointUp, ArcPoint, closestPointDown)
#geompy.addToStudy( Arc_1, 'Arc_1' )

listPoints = geompy.ExtractShapes(Partition_1, 
			geompy.ShapeType["VERTEX"], True)
pointsUp = getPointsFilter(listPoints, 'y', operator.ge, 0)
pointsDown = getPointsFilter(listPoints, 'y', operator.le, 0)
coordxUp = geompy.PointCoordinates(closestPointUp)[0]
coordxDown = geompy.PointCoordinates(closestPointDown)[0]
pointsUpRight = getPointsFilter(pointsUp, 'x', operator.ge, coordxUp)
pointsDownRight = getPointsFilter(pointsDown, 'x', operator.ge,coordxDown)

flapUp = geompy.MakePolyline(pointsUpRight)
flapDown = geompy.MakePolyline(pointsDownRight)

flap = geompy.MakeWire([Arc_1, flapUp, flapDown])
#geompy.addToStudy(flap, 'flap')


VertexVector = geompy.MakeVertexWithRef(ArcCenter, 0, 0, 1)
Vector = geompy.MakeVector(ArcCenter, VertexVector)
flapRot = geompy.MakeRotation(flap, Vector, angle*math.pi/180.0)
#geompy.addToStudy( flapRot, 'flapRot' )

Compound = geompy.MakeVertexOnLinesIntersection(Scale, flapRot)
interPoints = geompy.ExtractShapes(Compound, geompy.ShapeType["VERTEX"])
if getCoord(interPoints[0],'x') < getCoord(interPoints[1], 'x'):
	IntersectPoint = interPoints[0]
else:
	IntersectPoint = interPoints[1]
#geompy.addToStudy(IntersectPoint, 'IntersectPoint')

# Separate Points Up from Down

if angle>0:
	thresholdUp = getCoord(IntersectPoint,'x')
	thresholdDown = getCoord(closestPointDown, 'x')
else:
	thresholdUp = getCoord(closestPointUp, 'x')
	thresholdDown = getCoord(IntersectPoint, 'x')


# Line equation to separete flap up from flap down
m = np.tan(np.radians(angle-2))
EndVertex = geompy.MakeVertexOnCurve(Line_1, 0.5)
geompy.Rotate(EndVertex,Vector, np.radians(angle))
x1 = geompy.PointCoordinates(ArcCenter)[0]
y1 = geompy.PointCoordinates(ArcCenter)[1]
xend = geompy.PointCoordinates(EndVertex)[0]
yend = geompy.PointCoordinates(EndVertex)[1]
m = (yend-y1)/(xend-x1)
# Point-slope equation
def lineFunc(x):
	return m*(x-x1) + y1

listPoints = geompy.ExtractShapes(Partition_1, 
			geompy.ShapeType["VERTEX"], True)

pointsUp = (getPointsFilter(pointsUp, 'x', operator.le, thresholdUp))
pointsDown = (getPointsFilter(pointsDown, 'x', operator.le, thresholdDown))

listPointsFlap = geompy.ExtractShapes(flapRot, 
			geompy.ShapeType["VERTEX"], True)

pointsFlapUp = getPointsFilter(listPointsFlap, 'y', operator.gt, 
					0, lineFunc, 'x')
pointsFlapDown = getPointsFilter(listPointsFlap, 'y', operator.lt, 
					0, lineFunc, 'x')

pointsUp = pointsUp + getPointsFilter(pointsFlapUp, 'x', 
					operator.ge, thresholdUp)
pointsDown = pointsDown + getPointsFilter(pointsFlapDown, 'x', 
					operator.ge, thresholdDown)
	
nacaUp = geompy.MakePolyline(pointsUp)
nacaDown = geompy.MakePolyline(pointsDown)
#geompy.addToStudy(nacaUp, 'nacaUp')
#geompy.addToStudy(nacaDown, 'nacaDown')
geompy.ChangeOrientationShell(nacaDown)
naca = geompy.MakeWire([nacaUp, nacaDown], 1e-07)
offset = equidistance(naca, dist, True, extend=True)

listPointsNaca = geompy.ExtractShapes(naca, 
			geompy.ShapeType["VERTEX"], False)
listPointsOffset = geompy.ExtractShapes(offset, 
			geompy.ShapeType["VERTEX"], False)
naca = geompy.MakeInterpol(listPointsNaca)
offset = geompy.MakeInterpol(listPointsOffset)
geompy.addToStudy(naca, 'naca')
geompy.addToStudy(offset, 'offset')

[Vertex_1,Vertex_2] = geompy.SubShapes(naca, [2, 3])
[Vertex_3,Vertex_4] = geompy.SubShapes(offset, [3, 2])
Line_2 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_2)
Line_3 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
Line_4 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_4)
Line_5 = geompy.MakeLineTwoPnt(Vertex_3, Vertex_4)
Transversal = geompy.MakeCompound([Line_2,  Line_4])
RightBorder = geompy.MakeCompound([Line_3,  Line_5])
geompy.addToStudy(Transversal, 'transversal')
geompy.addToStudy(RightBorder, 'rightBorder')

try:
	geompy.Export(naca, ExportPath+'naca.step', "STEP")
	geompy.Export(offset, ExportPath+'offset.step', "STEP")
	geompy.Export(Transversal, ExportPath+'transversal.step', "STEP")
	geompy.Export(RightBorder, ExportPath+'rightBorder.step', "STEP")
except:
	print "Export Meshes Failed"


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
