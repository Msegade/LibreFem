SHELL:=/bin/bash

ifeq ($(DEBUG),True)
	DBGFLAG=--debug
endif

GEOMFILES=Skin.step Frame.step Stringer.step
MESHFILES=Skin.med Stringers.med Frames.med
RESULTS=static.resu static.rmed buckling.resu buckling.rmed
PARAMS=parameters.in

init: geometry.py mesh.py pre.comm analysis.comm
geometry: $(GEOMFILES)
mesh: $(MESHFILES)
pre: pre.mess
static: static.mess
buckling: buckling.mess
post: $(RESULTS)
postComp: results.json

# File initialization
geometry.py: $(PARAMS) geometry_t.py 
	jprepro $^ $@
mesh.py: $(PARAMS) mesh_t.py 
	jprepro $^ $@
pre.comm: $(PARAMS) pre_t.comm 
	jprepro $^ $@
analysis.comm: pre.comm static.comm buckling.comm 
	catAster pre.comm static.comm buckling.comm > analysis.comm

##########################################
#  Analysis pipeline
##########################################
$(GEOMFILES): geometry.py
	salome shell -- python $<

$(MESHFILES): mesh.py  $(GEOMFILES)
	salome shell -- python $<

####################################################
# Step by step resolution
####################################################

pre.mess: pre.export pre.comm $(MESHFILES)
	launchAster pre.comm pre.export 

static.mess: static.export static.comm pre.mess
	launchAster static.comm static.export 

static.resu static.rmed: pourStatic.export pourStatic.comm static.mess
	launchAster pourStatic.comm pourStatic.export 

buckling.mess: buckling.export buckling.comm static.mess
	launchAster buckling.comm buckling.export 

buckling.resu buckling.rmed: pourBuckling.export pourBuckling.comm buckling.mess
	launchAster pourBuckling.comm pourBuckling.export 

####################################################
# Complete in One file
####################################################

analysis.mess: analysis.export analysis.comm $(MESHFILES)
	launchAster analysis.comm analysis.export 

results.json: pourComp.export pourComp.comm analysis.mess
	launchAster pourComp.comm pourComp.export
####################################################

# Visualization
visualization: visualization.py post static.rmed buckling.rmed
	pvpython $<

# Cleaning
clean_init:
	rm -f geometry.py mesh.py pre.comm analysis.comm

clean_geometry:
	rm -f $(GEOMFILES)

clean_mesh:
	rm -f $(MESHFILES) 

clean_pre:
	rm -rf pre.mess pre.base

clean_static:
	rm -rf static.mess static.base

clean_buckling:
	rm -rf buckling.mess buckling.base

clean_results:
	rm -f $(RESULTS) pourStatic.mess pourBuckling.mess

clean_analysis:
	rm -rf analysis.mess analysis.base

clean_resultsComp:
	rm -f results.json pourComp.mess

clean_tmpFiles:
	rm -f *.tmp

clean: clean_init clean_geometry clean_mesh  clean_pre \
	   clean_static  clean_buckling \
	   clean_analysis \
	   clean_results clean_resultsComp \
	   clean_tmpFiles 
