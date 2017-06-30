SHELL:=/bin/bash

CAFLAGS=
ifeq ($(SILENT),True)
	NOOUTPUT=> /dev/null 2>&1
endif

TARGET=fuselage
MESHFILES=Skin.med  Stringers.med Frames.med
STEPFILES=Skin.step Frame.step Stringer.step
RESULTS=$(TARGET).resu $(TARGET).rmed 
PARAMS=parameters.in

init: geometry.py mesh.py $(TARGET).comm
geometry: $(STEPFILES)
mesh: $(MESHFILES)
solve: $(TARGET).mess
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

TARGTMP=$(TARGET).tmp
$(TARGET).mess: $(TARGET).export $(TARGET).comm $(MESHFILES) 
	cp $<  $(TARGTMP)
	as_run $(CAFLAGS) $(TARGTMP) $(NOOUTPUT)
	rm $(TARGTMP)

POURTMP=poursuite.tmp
$(RESULTS): poursuite.export poursuite.comm $(TARGET).mess
	cp $< $(POURTMP)
	as_run $(CAFLAGS) $(POURTMP) $(NOOUTPUT)
	rm $(POURTMP)

visualization: visualization.py post $(TARGET).rmed
	pvpython $<
##########################################

# Cleaning
clean_init:
	rm -f geometry.py mesh.py $(TARGET).comm

clean_geometry:
	rm -f $(STEPFILES)

clean_mesh:
	rm -f $(MESHFILES) Complete.med

clean_solve:
	rm -rf $(TARGET).mess $(TARGET).base

clean_results:
	rm -f $(RESULTS)

clean_tmpFiles:
	rm -f $(TARGTMP) $(POURTMP) *.mess

clean: clean_init clean_geometry clean_mesh clean_solve \
	   clean_results clean_tmpFiles 
