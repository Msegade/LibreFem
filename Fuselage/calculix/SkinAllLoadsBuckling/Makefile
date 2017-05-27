INPUT=main

all: main.frd

mesh.unv: onlySkin.py
	python $<

allinone.inp: mesh.unv
	unical -f $< allinone.inp 
	sed -i -e '/\*shell section/,+1d' allinone.inp

main.frd: $(INPUT).inp allinone.inp
	ccx $(INPUT)

clean:
	rm -f mesh.unv
	rm -f allinone.inp
	rm -f main.cvg main.dat main.frd main.sta spooles.out


