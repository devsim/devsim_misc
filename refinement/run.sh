#!/bin/bash
set -euxo pipefail
(time gmsh -2 -format 'msh2' gmsh_mos2d.geo 2>&1) 2>&1 | tee gmsh_mos2d_0.out
(time python mos2d_refine.py 2>&1) 2>&1 | tee mos2d_refine_0.out
cp gmsh_mos2d.msh gmsh_mos2d_0.msh
cp bgmesh.pos bgmesh_0.pos
cp test.dat test_0.dat

for i in 1 2 3; do 
(time gmsh -2 -format 'msh2' -o gmsh_mos2d_${i}.msh -bgm ./bgmesh.pos gmsh_mos2d.geo 2>&1) 2>&1 | tee gmsh_mos2d_${i}.out
cp gmsh_mos2d_${i}.msh gmsh_mos2d.msh
cp bgmesh.pos bgmesh_${i}.pos
cp test.dat test_${i}.dat
(time python mos2d_refine.py 2>&1) 2>&1 | tee mos2d_refine_${i}.out
done

