.PHONY: all
solve: fuselageStudy.rmed

skin.med stringers.med frames.med: complete.py
	python $<

fuselageStudy.rmed: fuselageStudy.export fuselage.comm \
					skin.med stringers.med frames.med 
	tmpfile=$<
	cp fuselageStudy.export "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

clean:
	rm -f skin.med stringers.med frames.med
	rm -f fuselageStudy.export.tmp
	rm -rf fuselageStudy.{rmed,base,resu,mess}

