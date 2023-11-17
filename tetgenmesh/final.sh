set -e
# ../tetgen1.5.1/tetgen -q1.2/50   -pAa test.poly && python load_tetgen.py  && python check_tetrahedra.py
#../tetgen1.5.1/tetgen -V -i -q   -pAa test.poly
#../tetgen1.5.1/tetgen -V -i -q   -pAa test.poly && python load_tetgen.py  && python check_tetrahedra.py
#../tetgen1.5.1/tetgen -q1.2/50   -pAa test.poly && python load_tetgen.py  && python check_tetrahedra.py
\rm -f test.a.node
\rm -f test.b.node test.b.ele test.b.mtr
python write_background.py
../tetgen1.5.1/tetgen -V -O7 -q -a -a 0.0001 -pA test.poly
python refine_tetgen.py
for i in 1; do
    for i in node ele mtr; do
        mv test.1.${i} test.b.${i}
    done
    ../tetgen1.5.1/tetgen -V -q -a -a 0.0001 -pmA test.poly
    python refine_tetgen.py
done
python load_tetgen.py
python check_tetrahedra.py
## TODO: come up with tolerance criteria based on element size too small

