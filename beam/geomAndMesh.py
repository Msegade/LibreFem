# -*- coding: utf-8 -*-


import salome
salome.salome_init()

#############Print results in current working directory###########
import os
currentpath=os.path.join(os.getcwd(), '')
ExportPATH=currentpath
##################################################################


###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

H = 20
W = 25
L = 200

OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
Face_1 = geompy.MakeFaceHW(H, W, 2)
Extrusion_1 = geompy.MakePrismVecH(Face_1, OX, L)
[Load,Fix] = geompy.SubShapes(Extrusion_1, [20, 31])
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( Face_1, 'Face_1' )
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )
geompy.addToStudyInFather( Extrusion_1, Load, 'Load' )
geompy.addToStudyInFather( Extrusion_1, Fix, 'Fix' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(salome.myStudy)

Local_Length_1 = smesh.CreateHypothesis('LocalLength')
Local_Length_1.SetLength( 10 )
Local_Length_1.SetPrecision( 1e-07 )
Regular_1D = smesh.CreateHypothesis('Regular_1D')
Quadrangle_2D = smesh.CreateHypothesis('Quadrangle_2D')

Mesh_1 = smesh.Mesh(Extrusion_1)
status = Mesh_1.AddHypothesis(Local_Length_1)
status = Mesh_1.AddHypothesis(Regular_1D)
Hexa_3D = Mesh_1.Hexahedron(algo=smeshBuilder.Hexa)
status = Mesh_1.AddHypothesis(Quadrangle_2D)
isDone = Mesh_1.Compute()

# Create Mesh groups
Load_1 = Mesh_1.GroupOnGeom(Load,'Load',SMESH.FACE)
Fix_1 = Mesh_1.GroupOnGeom(Fix,'Fix',SMESH.FACE)
smesh.SetName(Mesh_1, 'Mesh_1')


Mesh_1.ExportMED( r''+ExportPATH+'code_aster/'+'beam.mmed', 0, SMESH.MED_V2_2 , 1 )
Mesh_1.ExportUNV( r''+ExportPATH+'calculix/'+'beam.unv')
