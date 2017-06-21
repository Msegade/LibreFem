# -*- coding: iso-8859-1 -*-


import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import os

ExportPath=os.path.join(os.getcwd(),'')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

naca = geompy.ImportSTEP(ExportPath+"/naca.step")
offset = geompy.ImportSTEP(ExportPath+"/offset.step")
rightBorder = geompy.ImportSTEP(ExportPath+"/rightBorder.step")
transversal = geompy.ImportSTEP(ExportPath+"/transversal.step")


cw = 914.4
dist = 10

geomObj = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(-7*cw, -5*cw)
sk.addSegmentRelative(25*cw, 0)
sk.addSegmentRelative(0, 10*cw)
sk.addSegmentRelative(-25*cw, 0)
sk.close()
Sketch_1 = sk.wire(geomObj)

sk = geompy.Sketcher2D()
sk.addPoint(-cw, -cw)
sk.addSegmentRelative(3*cw, 0)
sk.addSegmentRelative(0, 2*cw)
sk.addSegmentRelative(-3*cw, 0)
sk.close()
Sketch_2 = sk.wire(geomObj)

point1 = geompy.MakeVertex(2*cw, cw, 0)
point2 = geompy.MakeVertexWithRef(point1, 10*cw, cw, 0)
point3 = geompy.MakeVertexWithRef(point2, 0, -4*cw, 0)
point4 = geompy.MakeVertexWithRef(point3, -10*cw, cw, 0)
wakeTop = geompy.MakeLineTwoPnt(point1, point2)
wakeBottom = geompy.MakeLineTwoPnt(point4, point3)
wakeRight = geompy.MakeLineTwoPnt(point2, point3)

Face_1 = geompy.MakeFaceWires([Sketch_1], 1)
[Edge_1] = geompy.SubShapes(rightBorder, [3])
Face_2 = geompy.MakeFaceWires([naca, Edge_1], 1)
Cut = geompy.MakeCutList(Face_1, [Face_2], True)

Partition = geompy.MakePartition([offset, rightBorder, transversal, 
				  Sketch_1, Sketch_2, 
				  wakeTop, wakeBottom, wakeRight, Cut], 
				  Limit=geompy.ShapeType["SHELL"],)

#wake_buffer = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
#geompy.UnionIDs(wake_buffer, [13, 16, 24, 41])
def getSubEdgesIDsByShape(Partition, shape):
    func = geompy.GetEdgeNearPoint
    edges = geompy.ExtractShapes(shape, 
			        geompy.ShapeType["EDGE"], False)
    # If shape is a line the edge is the shape
    if edges==[]:
            edges = [shape]
    points = []
    for edge in edges:
        points.append(geompy.MakeVertexOnCurve(edge, 0.5))
    subshapes = []
    for point in points:
        shapeTmp = func(Partition, point)
        subshapes.append(geompy.GetSubShapeID(Partition, shapeTmp))
    return subshapes

def getSubEdgeIDsByCoords(Partition, coordx, coordy, coordz):
    vertex = geompy.MakeVertex(coordx, coordy, coordz)
    func = geompy.GetEdgeNearPoint
    shape = func(Partition, vertex)
    edgeID = geompy.GetSubShapeID(Partition, shape)
    return edgeID



wake_buffer = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(wake_buffer, getSubEdgesIDsByShape(Partition, Sketch_2))

inlet = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(inlet, [getSubEdgeIDsByCoords(Partition, -7*cw, 0, 0)])

outlet = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(outlet, [getSubEdgeIDsByCoords(Partition, 18*cw, 0, 0)])

wake_top_bottom = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(wake_top_bottom, getSubEdgesIDsByShape(Partition, wakeTop))
geompy.UnionIDs(wake_top_bottom, getSubEdgesIDsByShape(Partition, wakeBottom))

wake_right = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(wake_right, getSubEdgesIDsByShape(Partition, wakeRight))

upper_wall = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(upper_wall, [getSubEdgeIDsByCoords(Partition, 12*cw, 5*cw, 0)])

lower_wall = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(lower_wall, [getSubEdgeIDsByCoords(Partition, 12*cw, -5*cw, 0)])

domain = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(domain, getSubEdgesIDsByShape(Partition, Sketch_1))

naca_g = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(naca_g, getSubEdgesIDsByShape(Partition, naca))
[line_1, line_2] = geompy.ExtractShapes(rightBorder, 
			        geompy.ShapeType["EDGE"], False)
geompy.UnionIDs(naca_g, getSubEdgesIDsByShape(Partition, line_1))

naca_spline = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(naca_spline, getSubEdgesIDsByShape(Partition, naca))
geompy.UnionIDs(naca_spline, getSubEdgesIDsByShape(Partition, offset))

naca_right_border = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(naca_right_border, getSubEdgesIDsByShape(Partition, rightBorder))

transversal_g = geompy.CreateGroup(Partition, geompy.ShapeType["EDGE"])
geompy.UnionIDs(transversal_g, getSubEdgesIDsByShape(Partition, transversal))

wake_buffer_F = geompy.CreateGroup(Partition, geompy.ShapeType["FACE"])
geompy.UnionIDs(wake_buffer_F, [39])
domain_F = geompy.CreateGroup(Partition, geompy.ShapeType["FACE"])
geompy.UnionIDs(domain_F, [2])
wake_F = geompy.CreateGroup(Partition, geompy.ShapeType["FACE"])
geompy.UnionIDs(wake_F, [43])

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( naca, 'naca' )
geompy.addToStudy( offset, 'offset' )
geompy.addToStudy( rightBorder, 'rightBorder' )
geompy.addToStudy( transversal, 'transversal' )
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( Sketch_2, 'Sketch_2' )
geompy.addToStudy( wakeTop, 'wakeTop' )
geompy.addToStudy( wakeBottom, 'wakeBottom' )
geompy.addToStudy( wakeRight, 'wakeRight' )
geompy.addToStudy( Partition, 'Partition' )
geompy.addToStudyInFather( Partition, wake_buffer, 'wake_buffer' )
geompy.addToStudyInFather( Partition, inlet, 'inlet' )
geompy.addToStudyInFather( Partition, wake_top_bottom, 'wake_top_bottom' )
geompy.addToStudyInFather( Partition, outlet, 'outlet' )
geompy.addToStudyInFather( Partition, wake_right, 'wake_right' )
geompy.addToStudyInFather( Partition, upper_wall, 'upper_wall' )
geompy.addToStudyInFather( Partition, domain, 'domain' )
geompy.addToStudyInFather( Partition, lower_wall, 'lower_wall' )
geompy.addToStudyInFather( Partition, wake_buffer_F, 'wake_buffer' )
geompy.addToStudyInFather( Partition, domain_F, 'domain' )
geompy.addToStudyInFather( Partition, wake_F, 'wake' )
geompy.addToStudyInFather( Partition, naca_g, 'naca' )
geompy.addToStudyInFather( Partition, naca_spline, 'naca_spline' )
geompy.addToStudyInFather( Partition, naca_right_border, 'naca_right_border' )
geompy.addToStudyInFather( Partition, transversal_g, 'transversal' )


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh = smesh.Mesh(Partition)
Quadrangle_2D = Mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)

####################################
# 1D Meshes
###################################
# Wake Buffer
Regular_1D = Mesh.Segment(geom=wake_buffer)
Local_Length_50 = Regular_1D.LocalLength(50,[],1e-07)

# Wake Top Bottom
Start_and_End_Length_1 = smesh.CreateHypothesis('StartEndLength')
Start_and_End_Length_1.SetStartLength( 50 )
Start_and_End_Length_1.SetEndLength( 100 )
Start_and_End_Length_1.SetReversedEdges( [] )
Start_and_End_Length_1.SetObjectEntry( 'Partition' )
status = Mesh.AddHypothesis(Regular_1D,wake_top_bottom)
status = Mesh.AddHypothesis(Start_and_End_Length_1,wake_top_bottom)

# Wake Right
Local_Length_100 = smesh.CreateHypothesis('LocalLength')
Local_Length_100.SetLength( 100 )
Local_Length_100.SetPrecision( 1e-07 )
status = Mesh.AddHypothesis(Regular_1D,wake_right)
status = Mesh.AddHypothesis(Local_Length_100,wake_right)

# Domain
Local_Length_300 = smesh.CreateHypothesis('LocalLength')
Local_Length_300.SetLength( 300 )
Local_Length_300.SetPrecision( 1e-07 )
status = Mesh.AddHypothesis(Regular_1D,domain)
status = Mesh.AddHypothesis(Local_Length_300,domain)

# Naca Spline
Nb_Segments_400 = smesh.CreateHypothesis('NumberOfSegments')
Nb_Segments_400.SetNumberOfSegments( 400 )
Nb_Segments_400.SetDistrType( 0 )
status = Mesh.AddHypothesis(Regular_1D,naca_spline)
status = Mesh.AddHypothesis(Nb_Segments_400,naca_spline)

# Naca Right Border
Nb_Segments_2 = smesh.CreateHypothesis('NumberOfSegments')
Nb_Segments_2.SetNumberOfSegments( 3 )
Nb_Segments_2.SetDistrType( 0 )
status = Mesh.AddHypothesis(Regular_1D,naca_right_border)
status = Mesh.AddHypothesis(Nb_Segments_2,naca_right_border)

# Naca Transversal
Nb_Segments_3 = smesh.CreateHypothesis('NumberOfSegments')
Nb_Segments_3.SetNumberOfSegments( 3 )
Nb_Segments_3.SetDistrType( 0 )
status = Mesh.AddHypothesis(Regular_1D,transversal_g)
status = Mesh.AddHypothesis(Nb_Segments_3,transversal_g)



####################################
# 2D Meshes
###################################

NETGEN_2D_ONLY = Mesh.Triangle(algo=smeshBuilder.NETGEN_2D,geom=wake_F)
NETGEN_2D_Parameters = NETGEN_2D_ONLY.Parameters()
NETGEN_2D_Parameters.SetMaxSize( 100 )
NETGEN_2D_Parameters.SetOptimize( 1 )
NETGEN_2D_Parameters.SetFineness( 5 )
NETGEN_2D_Parameters.SetGrowthRate( 0.005 )
NETGEN_2D_Parameters.SetNbSegPerEdge( 6.94726e-310 )
NETGEN_2D_Parameters.SetNbSegPerRadius( 2.29759e-316 )
NETGEN_2D_Parameters.SetMinSize( 50 )
NETGEN_2D_Parameters.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters.SetQuadAllowed( 0 )
NETGEN_2D_Parameters.SetSecondOrder( 0 )
NETGEN_2D_Parameters.SetFuseEdges( 48 )

NETGEN_2D_Parameters_2 = smesh.CreateHypothesis('NETGEN_Parameters_2D_ONLY', 'NETGENEngine')
NETGEN_2D_Parameters_2.SetMaxSize( 300 )
NETGEN_2D_Parameters_2.SetOptimize( 1 )
NETGEN_2D_Parameters_2.SetFineness( 3 )
NETGEN_2D_Parameters_2.SetMinSize( 50 )
NETGEN_2D_Parameters_2.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_2.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_2.SetSecondOrder( 0 )
NETGEN_2D_Parameters_2.SetFuseEdges( 48 )
status = Mesh.AddHypothesis(NETGEN_2D_ONLY,domain_F)
status = Mesh.AddHypothesis(NETGEN_2D_Parameters_2,domain_F)

NETGEN_2D_Parameters_3 = smesh.CreateHypothesis('NETGEN_Parameters_2D_ONLY', 'NETGENEngine')
NETGEN_2D_Parameters_3.SetMaxSize( 50 )
NETGEN_2D_Parameters_3.SetOptimize( 1 )
NETGEN_2D_Parameters_3.SetFineness( 3 )
NETGEN_2D_Parameters_3.SetMinSize( 2.6 )
NETGEN_2D_Parameters_3.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_3.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_3.SetSecondOrder( 0 )
NETGEN_2D_Parameters_3.SetFuseEdges( 48 )
status = Mesh.AddHypothesis(NETGEN_2D_ONLY,wake_buffer_F)
status = Mesh.AddHypothesis(NETGEN_2D_Parameters_3,wake_buffer_F)

isDone = Mesh.Compute()

upper_wall = Mesh.GroupOnGeom(upper_wall,'upper_wall',SMESH.EDGE)
lower_wall = Mesh.GroupOnGeom(lower_wall,'lower_wall',SMESH.EDGE)
inlet      = Mesh.GroupOnGeom(inlet,'inlet',SMESH.EDGE)
outlet     = Mesh.GroupOnGeom(outlet,'outlet',SMESH.EDGE)
naca_g       = Mesh.GroupOnGeom(naca_g,'naca',SMESH.EDGE)

# Extrusion
[ upper_wall_extruded, lower_wall_extruded, inlet_extruded, outlet_extruded, naca_extruded, upper_wall_top, lower_wall_top, inlet_top, outlet_top, naca_top ] = Mesh.ExtrusionSweepObject2D( Mesh, [ 0, 0, 2.5 ], 1 ,True)

# Lateral Faces
# Referenc elements of each face
face_up = Mesh.FindElementsByPoint(0, 100, 2.5, SMESH.FACE )
face_down = Mesh.FindElementsByPoint(0, 100, 0, SMESH.FACE )
aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_CoplanarFaces,
				SMESH.FT_Undefined, 
				face_up[0],SMESH.FT_Undefined,
				SMESH.FT_LogicalOR)
aCriteria.append(aCriterion)
aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_CoplanarFaces,
				SMESH.FT_Undefined, 
				face_down[0])
aCriteria.append(aCriterion)
aFilter_1 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_1.SetMesh(Mesh.GetMesh())
lateral_faces = Mesh.GroupOnFilter( SMESH.FACE, 'lateral_faces', aFilter_1 )
lateral_faces.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
smesh.SetName(lateral_faces, 'lateral_faces')

Mesh.GetGroupByName('upper_wall_extruded')[0].SetName('upper_wall')
Mesh.GetGroupByName('lower_wall_extruded')[0].SetName('lower_wall')
Mesh.GetGroupByName('inlet_extruded')[0].SetName('inlet')
Mesh.GetGroupByName('outlet_extruded')[0].SetName('outlet')
Mesh.GetGroupByName('naca_extruded')[0].SetName('naca')

SubMesh_1 = Regular_1D.GetSubMesh()
SubMesh_2 = Mesh.GetSubMesh( wake_top_bottom, 'SubMesh_2' )
SubMesh_3 = Mesh.GetSubMesh( wake_right, 'SubMesh_3' )
SubMesh_4 = Mesh.GetSubMesh( domain, 'SubMesh_4' )
SubMesh_5 = Mesh.GetSubMesh( naca_spline, 'SubMesh_5' )
SubMesh_6 = Mesh.GetSubMesh( naca_right_border, 'SubMesh_6' )
SubMesh_7 = Mesh.GetSubMesh( transversal_g, 'SubMesh_7' )
SubMesh_8 = NETGEN_2D_ONLY.GetSubMesh()
SubMesh_9 = Mesh.GetSubMesh( domain_F, 'SubMesh_9' )
SubMesh_10 = Mesh.GetSubMesh( wake_buffer_F, 'SubMesh_10' )

for group in Mesh.GetGroups():
        if group.GetType() == SMESH.EDGE:
            Mesh.RemoveGroup(group) 

## Set names of Mesh objects
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Start_and_End_Length_1, 'Start and End Length_1')
smesh.SetName(Local_Length_100, 'Local Length_100')
smesh.SetName(Local_Length_50, 'Local Length_50')
smesh.SetName(Nb_Segments_2, 'Nb. Segments_2')
smesh.SetName(Nb_Segments_3, 'Nb. Segments_3')
smesh.SetName(Local_Length_300, 'Local Length_300')
smesh.SetName(Nb_Segments_400, 'Nb. Segments_400')
smesh.SetName(NETGEN_2D_Parameters, 'NETGEN 2D Parameters')
smesh.SetName(NETGEN_2D_Parameters_2, 'NETGEN 2D Parameters_2')
smesh.SetName(NETGEN_2D_Parameters_3, 'NETGEN 2D Parameters_3')
smesh.SetName(Mesh.GetMesh(), 'Mesh')
smesh.SetName(SubMesh_1, 'SubMesh_1')
smesh.SetName(SubMesh_2, 'SubMesh_2')
smesh.SetName(SubMesh_3, 'SubMesh_3')
smesh.SetName(SubMesh_4, 'SubMesh_4')
smesh.SetName(SubMesh_5, 'SubMesh_5')
smesh.SetName(SubMesh_6, 'SubMesh_6')
smesh.SetName(SubMesh_7, 'SubMesh_7')
smesh.SetName(SubMesh_8, 'SubMesh_8')
smesh.SetName(SubMesh_9, 'SubMesh_9')
smesh.SetName(SubMesh_10, 'SubMesh_10')
smesh.SetName(upper_wall, 'upper_wall')
smesh.SetName(lower_wall, 'lower_wall')
smesh.SetName(inlet, 'inlet')
smesh.SetName(outlet, 'outlet')
smesh.SetName(naca, 'naca')

try:
	Mesh.ExportUNV( ExportPath+'Mesh.unv')
except:
	print "Failed Exporting Mesh"


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
