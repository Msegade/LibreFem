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

salome.salome_init()
theStudy = salome.myStudy

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import numpy as np
import SALOMEDS

geompy = geomBuilder.New(theStudy)

# Parameters
Diameter = {{Diameter}}
R = Diameter/2.0
length = {{length}}

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

Skin = geompy.ImportSTEP(ExportPATH+'Skin.step', False, True)
[Fix,SurfaceForce,Edge_3] = geompy.ExtractShapes(Skin, geompy.ShapeType["EDGE"], True)

# Frame import and cut
Frame = geompy.ImportSTEP(ExportPATH+'Frame.step', False, True)
# Cut by a plane to avoid problems during meshing
Plane_1 = geompy.MakePlane(O, OY, Diameter*2)
Frame = geompy.MakePartition([Frame], [Plane_1], [], [], geompy.ShapeType["SHELL"], 0, [], 0)
[FrameContact1,face_1,face_2, face_3, face_4, FrameContact2] = \
            geompy.ExtractShapes(Frame, geompy.ShapeType["FACE"], True)
FrameContact = geompy.CreateGroup(Frame, geompy.ShapeType["FACE"])
id1 = geompy.GetSubShapeID(Frame, FrameContact1)
id2 = geompy.GetSubShapeID(Frame, FrameContact2)
geompy.UnionIDs(FrameContact, [id1, id2])

# Stringer 
Stringer = geompy.ImportSTEP(ExportPATH+'Stringer.step', False, True)
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
nStringers = {{nStringers}}
nFrames = {{nFrames}}
frameMeshSize = {{frameMeshSize}}
stringerMeshSize = {{stringerMeshSize}}
skinMeshSize = {{skinMeshSize}}

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
SkinElements = Skin.CreateEmptyGroup( SMESH.FACE, 'SkinElements' )
nbAdd = SkinElements.AddFrom( Skin.GetMesh() )
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
#Quadrangle_2D_Frame = Frame.Quadrangle(algo=smeshBuilder.QUADRANGLE)
isDone = Frame.Compute()
#Frame.MergeNodes([[ 1, 4 ], [ 2, 3 ], [ 5, 6 ], [ 7, 8 ]], [])
FrameContactNodes = Frame.GroupOnGeom(FrameContact,
                            'FrameContactNodes',SMESH.NODE)
FrameContactEdges = Frame.GroupOnGeom(FrameContact,
                            'FrameContactEdges',SMESH.EDGE)
FrameContactElements = Frame.GroupOnGeom(FrameContact,
                            'FrameContactElements',SMESH.FACE)
FrameElements = Frame.CreateEmptyGroup( SMESH.FACE, 'FrameElements' )
nbAdd = FrameElements.AddFrom( Frame.GetMesh() )

FrameMeshes = [Frame]
increment = (length-0.04) / nFrames
for i in range(1, nFrames+1):
    FrameMeshes.append(Frame.TranslateObjectMakeMesh( Frame, 
                [ 0, 0, i*increment ], 1, 'Frame_translated' ))

Frames = smesh.Concatenate(FrameMeshes, 1, 1, 1e-05,False, 'Frames')

try:
  Skin.ExportMED( r''+ExportPATH+'Skin.med', 0, SMESH.MED_V2_2, 1, None ,1)
  Stringers.ExportMED( r''+ExportPATH+'Stringers.med', 0, SMESH.MED_V2_2, 1, None ,1)
  Frames.ExportMED( r''+ExportPATH+'Frames.med', 0, SMESH.MED_V2_2, 1, None ,1)
except:
  print 'ExportToMEDX() failed. Invalid file name?'

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
