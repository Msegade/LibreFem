.PHONY: all
all: post
mesh: linearMesh.med
solve: fuselageStudy.base
poursuite: poursuite.rmed

linearMesh.med: onlySkin.py
	python $<

fuselageStudy.base: fuselageStudy.export linearMesh.med fuselage.comm
	tmpfile=$<
	cp fuselageStudy.export "$tmpfile"
	-as_run "$tmpfile"
	rm "$tmpfile"

poursuite.rmed: poursuiteStudy.export poursuite.comm fuselageStudy.base
	tmpfile=$<
	cp poursuiteStudy.export "$tmpfile"
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
	rm -f poursuite.{resu, mess}
	rm -f mpfile

