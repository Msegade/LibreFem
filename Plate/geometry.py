# -*- coding: utf-8 -*-
import salome
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import SMESH
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(salome.myStudy)
import math

#############Print results in current working directory###########
import os
currentpath=os.path.join(os.getcwd(), '')
ExportPATH=currentpath
##################################################################

#===================================================
#                  GEOMETRY
#                  --------
#===================================================

R = 0.01
L = 0.05
W = 0.05

# Utilisation du Sketcher 2D
sketch="Sketcher:F 0 %f:TT 0 %f:TT %f %f:TT %f 0:TT "\
                    "%f 0:R -90:C %f 90" %  (R, L, W, L, W, R, R )


Wire_1 = geompy.MakeSketcher(sketch, [0, 0, 0, 0, 0, 1, 1, 0, -0])

Plate = geompy.MakeFaceWires([Wire_1], 1)
[left,hole,up,down,right] = geompy.SubShapeAllSorted(Plate, 
                                    geompy.ShapeType["EDGE"])
A=geompy.MakeVertex(R,0,0)
GA=geompy.GetVertexNearPoint(Plate,A)
B=geompy.MakeVertex(W,0,0)
GB=geompy.GetVertexNearPoint(Plate,B)
D=geompy.MakeVertex(W,L,0)
GD=geompy.GetVertexNearPoint(Plate,D)
F=geompy.MakeVertex(0,L,0)
GF=geompy.GetVertexNearPoint(Plate,F)
G=geompy.MakeVertex(0,R,0)
GG=geompy.GetVertexNearPoint(Plate,G)

geompy.addToStudy(Plate,"Plate")
geompy.addToStudyInFather(Plate,hole,"hole")
geompy.addToStudyInFather(Plate,left,"left")
geompy.addToStudyInFather(Plate,right,"right")
geompy.addToStudyInFather(Plate,down,"down")
geompy.addToStudyInFather(Plate,up,"up")
geompy.addToStudyInFather(Plate,GA,"A")
geompy.addToStudyInFather(Plate,GB,"B")
geompy.addToStudyInFather(Plate,GD,"D")
geompy.addToStudyInFather(Plate,GF,"F")
geompy.addToStudyInFather(Plate,GG,"G")
