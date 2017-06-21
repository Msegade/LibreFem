STEPFILES=naca.step offset.step rightBorder.step transversal.step

MESHFILES=Mesh.unv

geometry: $(STEPFILES)
mesh: constant/polyMesh
all: mesh

$(STEPFILES): geometry.py
	runSalome -t $<

$(MESHFILES): mesh.py $(STEPFILES)
	runSalome -t $<

constant/polyMesh:  $(MESHFILES) boundary.py
	ideasUnvToFoam $<
	transformPoints -scale "(0.001 0.001 0.001)"
	python boundary.py

0/U: velocity.py
	python $<
	
clean:
	rm -f $(STEPFILES)
	rm -f $(MESHFILES)
	rm -rf constant/polyMesh


