# Mass synchronization

+ Static Analysis
+ 3D Elements
+ Distributed load

 File                                   | Contents    
 :-------------                         | :-------------
 [geomAndMesh.py](geomAndMesh.py)       | Salome script to generate the geometry and mesh

## Model Description

The model is a cantilever beam with a rectangular cross section, 
with a distributed load on the top face

Parameters   | Value
:----------  | :-------------
P            | 0.5 MPa
L            | 200 mm
W            | 25 mm
H            | 20 mm

## Reference Solution


## PreProcessing

The geometry and mesh are genereated with the salome script [geomAndMesh.py](geomAndMesh.py)
    
## Solving
    
### Code_Aster

To launch the study:
```
$ as_run beamStudy.export
```

### Calculix

To launch the study:
```
$ ccx beam
```

## Postprocessing
