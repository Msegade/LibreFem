TARGET=fuselage
MESHFILES=Mesh.med
STEPFILES=Skin.step
RESULTS=$(TARGET).resu $(TARGET).rmed $(TARGET)Cyl.rmed

geometry: $(STEPFILES)
mesh: $(MESHFILES)
solve: $(TARGET).base
post: $(RESULTS)

$(STEPFILES): geometry.py
	python $<

$(MESHFILES): mesh.py $(STEPFILES)
	python $<

$(TARGET).base: $(TARGET).export $(TARGET).comm $(MESHFILES) 
	tmpfile=$<.tmp
	cp $< "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

$(RESULTS): poursuite.export fuselage.base
	tmpfile=$<
	cp $< "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

#displacements.png: postpro.py fuselageStudy.rmed
#	pvpython $<

clean_geometry:
	rm -f $(STEPFILES)

clean_mesh:
	rm -f $(MESHFILES)

clean_solve:
	rm -rf $(TARGET).base

clean_results:
	rm -f $(RESULTS)

clean_tmpFiles:
	rm -f $(TARGET).tmp poursuite.tmp mpfile *.mess


clean: clean_geometry clean_mesh clean_solve clean_results \
	   clean_tmpFiles
