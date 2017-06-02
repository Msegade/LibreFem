.PHONY: all
all: post
mesh: linearMesh.med
solve: fuselageStudy.rmed

linearMesh.med: onlySkin.py
	python $<

fuselageStudy.rmed: fuselageStudy.export linearMesh.med fuselage.comm
	tmpfile=$<
	cp fuselageStudy.export "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

post: postpro.py fuselageStudy.rmed
	pvpython $<

clean:
	rm -f linearMesh.med
	rm -f fuselageStudy.export.tmp
	rm -rf fuselageStudy.{rmed,base,resu,mess}
	rm -f  fuselageStudyCyl.rmed
	rm -f displacements.png

