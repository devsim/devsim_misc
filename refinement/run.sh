#!/bin/bash
set -e
gmsh -2 -format 'msh2' gmsh_mos2d.geo
python mos2d_refine.py
#gmsh -2 -format 'msh2' -bgm ./bgmesh.pos -merge gmsh_mos2d.geo
#python mos2d_refine.py
#gmsh -2 -format 'msh2' -bgm ./bgmesh.pos -merge gmsh_mos2d.geo
#python mos2d_refine.py
for i in 1, 2, 3, 4, 5, 6, 7, 8, 9, 10; do 
#for i in 1, 2, 3; do 
#gmsh -2 -format 'msh2' -bgm ./bgmesh.pos  gmsh_mos2d.geo
gmsh -2 -format 'msh2' -bgm ./bgmesh.pos -merge gmsh_mos2d.geo
python mos2d_refine.py
done
