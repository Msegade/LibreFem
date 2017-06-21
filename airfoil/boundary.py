#! /usr/bin/python
 
  
import sys
 
from PyFoam.RunDictionary.ParsedParameterFile import ParsedBoundaryDict

fName='constant/polyMesh/boundary'
f = ParsedBoundaryDict(fName)
f["naca"]["type"] = "wall"
f["lateral_faces"]["type"] = "empty"

f.writeFile()
