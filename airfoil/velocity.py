#! /usr/bin/python
 
  
import sys
import numpy as np
 
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

velocity = 57.7
angle = 4

angle = np.radians(4)
vx = velocity*np.cos(angle)
vy = velocity*np.sin(angle)

fName='0/U'
f = ParsedParameterFile(fName)
if angle>=0:
    patch = 'upper_wall'
else:
    patch = 'lower_wall'

f["internalField"] = 'uniform (%f %f 0)' % (vx, vy)
f["boundaryField"]["inlet"]["value"] = 'uniform (%f %f 0)' % (vx, vy)
f["boundaryField"][patch]["value"] = 'uniform (%f %f 0)' % (vx, vy)

f.writeFile()


