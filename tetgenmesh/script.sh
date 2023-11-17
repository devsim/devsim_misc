set -e
# ../tetgen1.5.1/tetgen -q1.2/50   -pAa test.poly && python load_tetgen.py  && python check_tetrahedra.py
#../tetgen1.5.1/tetgen -V -i -q   -pAa test.poly
#../tetgen1.5.1/tetgen -V -i -q   -pAa test.poly && python load_tetgen.py  && python check_tetrahedra.py
#../tetgen1.5.1/tetgen -q1.2/50   -pAa test.poly && python load_tetgen.py  && python check_tetrahedra.py
\rm -f test.a.node
python write_background.py
../tetgen1.5.1/tetgen -V -O7 -q2  -a 0.0001 -a -pA test.poly
#../tetgen1.5.1/tetgen -V -O7 -q -i  -pAa test.poly
#../tetgen1.5.1/tetgen -V -i -q1.2/30  -pAa test.poly
#../tetgen1.5.1/tetgen -V -i -q   -pAa test.poly
python load_tetgen.py
python check_tetrahedra.py

#\cp refine.node test.a.node
#../tetgen1.5.1/tetgen -V -O7 -q -i  -pAa test.poly
#python load_tetgen.py
#python check_tetrahedra.py
##TODO: add points at position of bad elements
#
#\cp refine.node test.a.node
#../tetgen1.5.1/tetgen -V -O7 -q -i  -pAa test.poly
#python load_tetgen.py
#python check_tetrahedra.py
#exit
