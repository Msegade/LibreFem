# -*- coding: utf-8 -*-

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

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

geompy = geomBuilder.New(theStudy)

# Parameters
Diameter = {{Diameter}}
R = Diameter/2.0
length = {{length}}
nStringers = {{nStringers}}
nFrames = {{nFrames}}

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
Frame = geompy.MakeRevolution(Sketch_1, OZ, math.radians(360))
Frame.SetColor(SALOMEDS.Color(1,0,0))

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
#geompy.addToStudyInFather( Frame, FrameContact, 'FrameContact' )
geompy.addToStudy( Stringer, 'Stringer' )
geompy.addToStudyInFather( Stringer, StringerContact, 'StringerContact' )

geompy.ExportSTEP(Skin, ExportPATH+'Skin.step', GEOM.LU_METER )
geompy.ExportSTEP(Frame, ExportPATH+'Frame.step', GEOM.LU_METER )
geompy.ExportSTEP(Stringer, ExportPATH+'Stringer.step', GEOM.LU_METER )

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
