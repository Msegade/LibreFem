#############Print results in current working directory###########
import os
currentpath=os.path.join(os.getcwd(), '')
ExportPATH=currentpath
##################################################################

import salome
salome.salome_init()
import pvsimple
from pvsimple import *
pvsimple._DisableFirstRenderCameraReset()

# Create a new 'MED Reader'
fuselageStudyrmed = MEDReader(FileName=ExportPATH+'fuselageStudy.rmed')

SetActiveSource(fuselageStudyrmed)
# Properties
fuselageStudyrmed.AllArrays = ['TS0/mesh/ComSup1/res1____DEPL@@][@@P1']
# Generate Vectors
fuselageStudyrmed.GenerateVectors = 1

# Get active view
renderView  = GetActiveViewOrCreate('RenderView')
#renderView  = CreateRenderView('RenderView')

# Show data in view
fuselageDisplay = Show(fuselageStudyrmed, renderView)

# Reset view to fit data
renderView.ResetCamera()

# set scalar coloring
ColorBy(fuselageDisplay, ('POINTS', 'res1____DEPL'))

# rescale color and/or opacity maps used to include current data range
fuselageDisplay.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
fuselageDisplay.SetScalarBarVisibility(renderView, True)

# get color transfer function/color map for 'res1DEPL'
res1DEPLLUT = GetColorTransferFunction('res1DEPL')

# get opacity transfer function/opacity map for 'res1DEPL'
res1DEPLPWF = GetOpacityTransferFunction('res1DEPL')

renderView.CameraViewUp = [1, 0.2, 0.1]
renderView.CameraFocalPoint = [0, 0, 3]
renderView.CameraViewAngle = 30
renderView.CameraPosition = [3.4,10.8,15]
renderView.CenterOfRotation = [0, -0.1, 3]
renderView.RotationFactor = 1
#renderView.ViewSize = [1920, 1080]

# show data in view
#Render()
#WriteImage("displacements.png")
if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
