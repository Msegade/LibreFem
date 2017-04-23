import bpy


# Generate a new curve
curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData.dimensions = '3D'
# Create a bezier curve
bcurve = curveData.splines.new('BEZIER')

# Points of the curve
points = [(1, 10, 1),
          (2, 5, 1),
          (7.7, 3.9, 1),
          (0, 2, 1) ]

# Map points to bezier curve
# Bezier curve starts with one point, we add n-1 points
bcurve.bezier_points.add(len(points)-1)
for i, point in enumerate(points):
    bcurve.bezier_points[i].co = points[i]


# Create the object
ob = bpy.data.objects.new('CurveObj', curveData)
# Link object to the scene
bpy.context.scene.objects.link(ob)
