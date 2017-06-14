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
length = 6.0
nStringers = 36
nFrames = 6

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
[StringerContact1,face_2, face_3, face_4, StringerContact2] = \
        geompy.ExtractShapes(Stringer, geompy.ShapeType["FACE"], True)

StringerContact = geompy.CreateGroup(Stringer, geompy.ShapeType["FACE"])
id1 = geompy.GetSubShapeID(Stringer, StringerContact1)
id2 = geompy.GetSubShapeID(Stringer, StringerContact2)
geompy.UnionIDs(StringerContact, [id1, id2])

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
geompy.addToStudyInFather( Stringer, StringerContact, 'StringerContact' )

###
### SMESH component
###


import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

# Parameters
frameMeshSize = 0.1
stringerMeshSize = 0.1
skinMeshSize = 0.07
smesh = smeshBuilder.New(theStudy)

# Skin Mesh 
Skin = smesh.Mesh(Skin)
Regular_1D_Skin = Skin.Segment()
Local_Length_Skin = Regular_1D_Skin.LocalLength(skinMeshSize,None,1e-07)
Quadrangle_2D = Skin.Quadrangle(algo=smeshBuilder.QUADRANGLE)
isDone = Skin.Compute()
FixNodes = Skin.GroupOnGeom(Fix,'FixNodes',SMESH.NODE)
FixEdges = Skin.GroupOnGeom(Fix,'FixEdges',SMESH.EDGE)
ForceNodes = Skin.GroupOnGeom(SurfaceForce,'ForceNodes',SMESH.NODE)
ForceEdges = Skin.GroupOnGeom(SurfaceForce,'ForceEdges',SMESH.EDGE)
PressureLoad = Skin.CreateEmptyGroup( SMESH.FACE, 'PressureLoad' )
nbAdd = PressureLoad.AddFrom( Skin.GetMesh() )
ShellElements = Skin.CreateEmptyGroup( SMESH.FACE, 'ShellElements' )
nbAdd = ShellElements.AddFrom( Skin.GetMesh() )
smesh.SetName(Skin, 'Skin')

# Master Node
nodeID = Skin.AddNode( 0, 0, length )
MNode = Skin.CreateEmptyGroup( SMESH.NODE, 'MNode' )
nbAdd = MNode.Add( [ nodeID ] )

# StringerMesh
Stringer = smesh.Mesh(Stringer)
Regular_1D_Stringer = Stringer.Segment()
Local_Length_Stringer = Regular_1D_Stringer.LocalLength(stringerMeshSize,None,1e-07)
Quadrangle_2D_Stringer = Stringer.Quadrangle(algo=smeshBuilder.QUADRANGLE)
isDone = Stringer.Compute()
StringerContactNodes = Stringer.GroupOnGeom(StringerContact,
                            'StringerContactNodes',SMESH.NODE)
StringerContactEdges = Stringer.GroupOnGeom(StringerContact,
                            'StringerContactEdges',SMESH.EDGE)
StringerContactElements = Stringer.GroupOnGeom(StringerContact,
                            'StringerContactElements',SMESH.FACE)
StringerElements = Stringer.CreateEmptyGroup( SMESH.FACE, 'StringerElements' )
nbAdd = StringerElements.AddFrom( Stringer.GetMesh() )

angle = np.radians(360/nStringers)
StringerMeshes = [Stringer]
for i in range(1, nStringers):
    StringerMeshes.append(Stringer.RotateObjectMakeMesh( Stringer, 
        SMESH.AxisStruct( 0, 0, 0, 0, 0, 1 ), angle*i , 1, 'Stringer%d' %(i+1)))

Stringers = smesh.Concatenate(StringerMeshes, 1, 1, 1e-05,False,'Stringers')

# FrameMesh
Frame = smesh.Mesh(Frame)
Regular_1D_Frame = Frame.Segment()
Local_Length_Frame = Regular_1D_Frame.LocalLength(frameMeshSize,None,1e-07)
Quadrangle_2D_Frame = Frame.Quadrangle(algo=smeshBuilder.QUAD_MA_PROJ)
isDone = Frame.Compute()
FrameContactNodes = Frame.GroupOnGeom(FrameContact,
                            'FrameContactNodes',SMESH.NODE)
FrameContactEdges = Frame.GroupOnGeom(FrameContact,
                            'FrameContactEdges',SMESH.EDGE)
FrameContactElements = Frame.GroupOnGeom(FrameContact,
                            'FrameContactElements',SMESH.FACE)
FrameElements = Frame.CreateEmptyGroup( SMESH.FACE, 'FrameElements' )
nbAdd = FrameElements.AddFrom( Frame.GetMesh() )

FrameMeshes = [Frame]
increment = length / nFrames
for i in range(1, nFrames+1):
    FrameMeshes.append(Frame.TranslateObjectMakeMesh( Frame, 
                [ 0, 0, i*increment ], 1, 'Frame_translated' ))

Frames = smesh.Concatenate(FrameMeshes, 1, 1, 1e-05,False, 'Frames')

try:
  Skin.ExportMED( r''+ExportPATH+'skin.med', 0, SMESH.MED_V2_2, 1, None ,1)
  Stringers.ExportMED( r''+ExportPATH+'stringers.med', 0, SMESH.MED_V2_2, 1, None ,1)
  Frames.ExportMED( r''+ExportPATH+'frames.med', 0, SMESH.MED_V2_2, 1, None ,1)
except:
  print 'ExportToMEDX() failed. Invalid file name?'

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
