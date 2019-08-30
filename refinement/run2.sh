#!/bin/bash
set -euxo pipefail
INNAME=gmsh_mos2d.geo
OUTMESH=gmsh_mos2d2
OUTBG=bgmesh2
REFINESCRIPT=mos2d_refine2
DBGMESH=test2

(time gmsh -2 -format 'msh2' ${INNAME} -o ${OUTMESH}.msh 2>&1) 2>&1 | tee ${OUTMESH}_0.out
(time python ${REFINESCRIPT}.py 2>&1) 2>&1 | tee ${REFINESCRIPT}_0.out
cp ${OUTMESH}.msh ${OUTMESH}_0.msh
cp ${OUTBG}.pos ${OUTBG}_0.pos
cp ${DBGMESH}.dat ${DBGMESH}_0.dat

for i in 1 2 3; do 
(time gmsh -2 -format 'msh2' -o ${OUTMESH}_${i}.msh -bgm ./${OUTBG}.pos ${INNAME} 2>&1) 2>&1 | tee ${OUTMESH}_${i}.out
cp ${OUTMESH}_${i}.msh ${OUTMESH}.msh
cp ${OUTBG}.pos ${OUTBG}_${i}.pos
cp ${DBGMESH}.dat ${DBGMESH}_${i}.dat
(time python ${REFINESCRIPT}.py 2>&1) 2>&1 | tee ${REFINESCRIPT}_${i}.out
done

