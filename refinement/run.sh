#!/bin/bash
set -e
gmsh -2 -format 'msh2' gmsh_mos2d.geo
python mos2d_refine.py
gmsh -2 -format 'msh2' -bgm ./mos2d_bgmesh.pos  gmsh_mos2d.geo
python mos2d_refine.py
gmsh -2 -format 'msh2' -bgm ./mos2d_bgmesh.pos  gmsh_mos2d.geo
python mos2d_refine.py
gmsh -2 -format 'msh2' -bgm ./mos2d_bgmesh.pos  gmsh_mos2d.geo

