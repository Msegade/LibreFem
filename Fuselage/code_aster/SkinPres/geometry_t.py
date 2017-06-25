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
Circle = geompy.MakeCircle(O, OZ, R)
Skin = geompy.MakePrismVecH(Circle, OZ, length)

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Circle, 'Circle' )
geompy.addToStudy( Skin, 'Skin' )

geompy.ExportSTEP(Skin, ExportPATH+'Skin.step', GEOM.LU_METER )
