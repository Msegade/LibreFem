#############Print results in current working directory###########
import os
currentpath=os.path.join(os.getcwd(), '')
ExportPATH=currentpath
##################################################################

import pvsimple
from pvsimple import *
#from paraview.simple import *

# Create a 'MED Reader'
fuselagermed = MEDReader(FileName=ExportPATH+'fuselage.rmed')

# Generate Vectors
fuselagermed.GenerateVectors = 1

fuselageDisplay = Show()
## set scalar coloring
ColorBy(fuselageDisplay, ('POINTS', 'res1____DEPL_Vector'))

Hide(fuselagermed)
# create a new 'ELNO Mesh'
eLNOMesh = ELNOMesh(Input=fuselagermed)

# show data in view
eLNOMeshDisplay = Show(eLNOMesh)

## Set scalar coloring
ColorBy(eLNOMeshDisplay, ('POINTS', 'res1____SIEQ_ELNO'))

## Reset view to fit data
ResetCamera()

Show()
Render()

