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
Circle = geompy.MakeCircle(O, OZ, R)
Skin = geompy.MakePrismVecH(Circle, OZ, length)
[Fix,SurfaceForce,Edge_3] = geompy.ExtractShapes(Skin, geompy.ShapeType["EDGE"], True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Circle, 'Circle' )
geompy.addToStudy( Skin, 'Skin' )
geompy.addToStudyInFather( Skin, Fix, 'Fix' )
geompy.addToStudyInFather( Skin, SurfaceForce, 'SurfaceForce' )

###
### SMESH component
###


import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

# Parameters
meshSize = 0.07

smesh = smeshBuilder.New(theStudy)
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

nodeID = Mesh_1.AddNode( 0, 0, length )
MNode = Mesh_1.CreateEmptyGroup( SMESH.NODE, 'MNode' )
nbAdd = MNode.Add( [ nodeID ] )

#Mesh_1.ConvertToQuadratic(0)

try:
  Mesh_1.ExportMED( r''+ExportPATH+'linearMesh.med', 0, SMESH.MED_V2_2, 1, None ,1)
except:
  print 'ExportToMEDX() failed. Invalid file name?'

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
