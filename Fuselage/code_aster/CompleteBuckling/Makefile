SHELL:=/bin/bash

ifeq ($(DEBUG),True)
	DBGFLAG=--debug
endif

TARGET=fuselage
MESHFILES=Skin.med  Stringers.med Frames.med
STEPFILES=Skin.step Frame.step Stringer.step
RESULTS=$(TARGET).resu $(TARGET).rmed results.json
PARAMS=parameters.in

init: geometry.py mesh.py $(TARGET).comm
geometry: $(STEPFILES)
mesh: $(MESHFILES)
solve: $(TARGET).mess
buckling: buckling.mess
post: $(RESULTS)
all: visualization

# File intialization
geometry.py: $(PARAMS) geometry_t.py 
	jprepro $^ $@
mesh.py: $(PARAMS) mesh_t.py 
	jprepro $^ $@
$(TARGET).comm: $(PARAMS) $(TARGET)_t.comm 
	jprepro $^ $@

#  Analysis pipeline
##########################################
$(STEPFILES): geometry.py
	python $<

$(MESHFILES): mesh.py $(STEPFILES)
	python $<

$(TARGET).mess: $(TARGET).export $(TARGET).comm $(MESHFILES) 
	launchAster $(DBGFLAG) $(TARGET).comm $(TARGET).export $(NOOUTPUT)

buckling.mess: buckling.export buckling.comm $(TARGET).mess
	launchAster $(DBGFLAG) buckling.comm buckling.export $(NOOUTPUT)

$(RESULTS): poursuite.export poursuite.comm $(TARGET).mess
	launchAster $(DBGFLAG) poursuite.comm poursuite.export $(NOOUTPUT)

##########################################

# Visualization
visualization: visualization.py post $(TARGET).rmed
	pvpython $<

# Cleaning
clean_init:
	rm -f geometry.py mesh.py $(TARGET).comm

clean_geometry:
	rm -f $(STEPFILES)

clean_mesh:
	rm -f $(MESHFILES) Complete.med

clean_solve:
	rm -rf $(TARGET).mess $(TARGET).base

clean_buckling:
	rm -rf buckling.mess buckling.base

clean_results:
	rm -f $(RESULTS) poursuite.mess results.json

clean_tmpFiles:
	rm -f $(TARGET).comm.tmp $(TARGET).export.tmp

clean: clean_init clean_geometry clean_mesh clean_solve \
	   clean_buckling clean_results clean_tmpFiles 
