.PHONY: all

MODEL = fuselage
GEOMETRY = onlySkin
MESH = linearMesh
POST = postpro

all: post
mesh: linearMesh.med
solve: fuselageStudy.rmed

$(MESH).med: $(GEOMETRY).py
	python $<

$(MODEL)Study.rmed: $(MODEL)Study.export $(MESH).med $(MODEL).comm
	tmpfile=$<.tmp
	cp $(MODEL)Study.export "$tmpfile"
	as_run "$tmpfile"
	rm "$tmpfile"

post: $(POST).py $(MODEL)Study.rmed
	pvpython $<

clean:
	rm -f $(MESH).med
	rm -f $(MODEL)Study.export.tmp
	rm -rf $(MODEL)Study.{rmed,base,resu,mess}
	rm -f  $(MODEL)StudyCyl.rmed

