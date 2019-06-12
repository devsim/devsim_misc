#!/bin/bash
set -e
#use pygmsh to create the structure
#no interfaces or boundaries are defined
#also creates ring.yaml which is used by test_convert script below
python ring.py
# create the initial mesh
gmsh -3 -format 'msh2' ring.geo
# python script to add interfaces and create new output mesh, test.msh
python test_convert.py  --input_mesh ring.msh  --output_mesh test.msh --yaml ./ring.yaml 
# use devsim to load structure from test.msh
python test.py

