# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v7.8.0 with dump python functionality
###

#############Print results in current working directory###########
import os
currentpath=os.path.join(os.getcwd(), '')
ExportPATH=currentpath
##################################################################


import sys
import salome
import numpy as np

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/miguel/Documents/MIEMA/Trabajo/LibreFem/Fuselage')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

geompy = geomBuilder.New(theStudy)

# Parameters
Diameter = 3.8
R = Diameter/2.0
length = 6

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# Skin
Circle = geompy.MakeCircle(O, OZ, R)
Skin = geompy.MakePrismVecH(Circle, OZ, length)
[Fix,SurfaceForce,Edge_3] = geompy.ExtractShapes(Skin, geompy.ShapeType["EDGE"], True)

# Frame
Extrusion_1_vertex_4 = geompy.GetSubShape(Skin, [4])
Plane_1 = geompy.MakePlane(Extrusion_1_vertex_4, OY, 2)
sk = geompy.Sketcher2D()
sk.addPoint(0.040000, 0.000000)
sk.addSegmentAbsolute(0.020000, 0.000000)
sk.addSegmentAbsolute(0.020000, -0.060000)
sk.addSegmentAbsolute(0.000000, -0.060000)
Sketch_1 = sk.wire(Plane_1)
Frame = geompy.MakeRevolution(Sketch_1, OZ, 360*math.pi/180.0)
Frame.SetColor(SALOMEDS.Color(1,0,0))
[face_1,face_2,FrameContact] = geompy.ExtractShapes(Frame, geompy.ShapeType["FACE"], True)

# Stringer
geomObj_3 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(-0.030000, -1.900000)
sk.addSegmentAbsolute(-0.010000, -1.900000)
sk.addSegmentAbsolute(-0.010000, -1.870000)
sk.addSegmentAbsolute(0.010000, -1.870000)
sk.addSegmentAbsolute(0.010000, -1.900000)
sk.addSegmentAbsolute(0.030000, -1.900000)
Sketch_2 = sk.wire(geomObj_3)
Stringer = geompy.MakePrismVecH(Sketch_2, OZ, 6)
Stringer.SetColor(SALOMEDS.Color(0,1,0))
[StringerContact1,face_2,face_3, face_4, StringerContact2] = \
        geompy.ExtractShapes(Stringer, geompy.ShapeType["FACE"], True)


geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Circle, 'Circle' )
geompy.addToStudy( Skin, 'Skin' )
geompy.addToStudyInFather( Skin, Fix, 'Fix' )
geompy.addToStudyInFather( Skin, SurfaceForce, 'SurfaceForce' )
geompy.addToStudy( Frame, 'Frame' )
geompy.addToStudyInFather( Frame, FrameContact, 'FrameContact' )
geompy.addToStudy( Stringer, 'Stringer' )
geompy.addToStudyInFather( Stringer, StringerContact1, 'StringerContact1' )
geompy.addToStudyInFather( Stringer, StringerContact2, 'StringerContact2' )

###
### SMESH component
###


import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

# Parameters
meshSize = 0.1
smesh = smeshBuilder.New(theStudy)

# Skin Mesh 
Mesh_1 = smesh.Mesh(Skin)
Regular_1D = Mesh_1.Segment()
Local_Length_1 = Regular_1D.LocalLength(meshSize,None,1e-07)
Quadrangle_2D = Mesh_1.Quadrangle(algo=smeshBuilder.QUADRANGLE)
isDone = Mesh_1.Compute()
FixNodes = Mesh_1.GroupOnGeom(Fix,'FixNodes',SMESH.NODE)
FixEdges = Mesh_1.GroupOnGeom(Fix,'FixEdges',SMESH.EDGE)
ForceNodes = Mesh_1.GroupOnGeom(SurfaceForce,'ForceNodes',SMESH.NODE)
ForceEdges = Mesh_1.GroupOnGeom(SurfaceForce,'ForceEdges',SMESH.EDGE)
PressureLoad = Mesh_1.CreateEmptyGroup( SMESH.FACE, 'PressureLoad' )
nbAdd = PressureLoad.AddFrom( Mesh_1.GetMesh() )
ShellElements = Mesh_1.CreateEmptyGroup( SMESH.FACE, 'ShellElements' )
nbAdd = ShellElements.AddFrom( Mesh_1.GetMesh() )
smesh.SetName(Mesh_1, 'Mesh_1')

# Master Node
nodeID = Mesh_1.AddNode( 0, 0, length )
MNode = Mesh_1.CreateEmptyGroup( SMESH.NODE, 'MNode' )
nbAdd = MNode.Add( [ nodeID ] )

nStringers = 36
# StringerMesh
Regular_1D_1_1 = smesh.CreateHypothesis( "Regular_1D" )
Quadrangle_2D_2_1 = smesh.CreateHypothesis( "Quadrangle_2D" )
Mesh_2 = smesh.Mesh(Stringer)
status = Mesh_2.AddHypothesis(Local_Length_1)
Regular_1D_1_2 = Mesh_2.Segment()
Quadrangle_2D_2_2 = Mesh_2.Quadrangle(algo=smeshBuilder.QUADRANGLE)
isDone = Mesh_2.Compute()
StringerContact1_1 = Mesh_2.GroupOnGeom(StringerContact1,'StringerContact1',SMESH.FACE)
StringerContact2_1 = Mesh_2.GroupOnGeom(StringerContact2,'StringerContact2',SMESH.FACE)
StringerContact1_2 = Mesh_2.GroupOnGeom(StringerContact1,'StringerContact1',SMESH.NODE)
StringerContact2_2 = Mesh_2.GroupOnGeom(StringerContact2,'StringerContact2',SMESH.NODE)
StringerContactNodes = Mesh_2.GetMesh().UnionListOfGroups([ StringerContact1_2, StringerContact2_2 ], 'StringerContactNodes' )
StringeContactElements = Mesh_2.GetMesh().UnionListOfGroups([ StringerContact1_1, StringerContact2_1 ], 'StringeContactElements' )
Mesh_2.RemoveGroup(StringerContact1_1)
Mesh_2.RemoveGroup(StringerContact2_1)
Mesh_2.RemoveGroup(StringerContact1_2)
Mesh_2.RemoveGroup(StringerContact2_2)

angle = np.radians(360/nStringers)
StringerMeshes = [Mesh_2]
for i in range(1, nStringers):
    StringerMeshes.append(Mesh_2.RotateObjectMakeMesh( Mesh_2, 
        SMESH.AxisStruct( 0, 0, 0, 0, 0, 1 ), angle*i , 1, 'Stringer%d' %(i+1)))


try:
  Mesh_1.ExportMED( r''+ExportPATH+'linearMesh.med', 0, SMESH.MED_V2_2, 1, None ,1)
except:
  print 'ExportToMEDX() failed. Invalid file name?'

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
