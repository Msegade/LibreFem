import bpy


# Generate a new curve
curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData.dimensions = '3D'
# Create a nurbs curve
bcurve = curveData.splines.new('NURBS')

# Points of the curve
points = [(1, 10, 1),
          (2, 5, 1),
          (7.7, 3.9, 1),
          (0, 2, 1) ]

# Map points to curve
bcurve.points.add(len(points))
for i, point in enumerate(points):
    x,y,z = points[i]
    bcurve.points[i].co = (x, y, z, 1)


# Create the object
ob = bpy.data.objects.new('CurveObj', curveData)
# Link object to the scene
bpy.context.scene.objects.link(ob)
