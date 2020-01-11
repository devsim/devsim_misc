
import pygmsh
import bool_common

geom = pygmsh.opencascade.Geometry(
    #characteristic_length_min=.1,
  #characteristic_length_max=2.5e-5
)

w=1
h=1
tox=3
tsi=60
xrf=-0.1
trf=3
l_contact=1


#tcl0=0.5   #cl in ox
#tcl1=0.05  #cl near interface
#tcl2=0.5
#tcl3=0.5   #cl near backside
lcar=0.3
lrf=0.1


gate=bool_common.create_box_volume(geom, h=h, w=w, l=l_contact, x=-tox-l_contact, z=0, lcar=lcar)
ox=bool_common.create_box_volume(geom, h=h, w=w, l=tox, x=-tox, z=0, lcar=lcar)
#rf=bool_common.create_box_volume(geom, h=h, w=w, l=trf, x=0, z=0, lcar=lcar)
si=bool_common.create_box_volume(geom, h=h, w=w, l=tsi, x=0, z=0, lcar=lcar)
sub=bool_common.create_box_volume(geom, h=h, w=w, l=l_contact, x=tsi, z=0, lcar=lcar)
all_volumes=[ox, si, gate, sub]
geom.boolean_fragments( all_volumes,[], delete_first=True, delete_other=False)
#['gate', 'sub', 'interface']
#['oxide', 'silicon']

geom.add_physical_volume(gate, 'gate')
geom.add_physical_volume(sub, 'sub')
geom.add_physical_volume(ox, 'ox')
geom.add_physical_volume(si, 'si')

# TODO: add refinement box
# 
mydict = {
    "lrf" : lrf,
  "lcar" : lcar,
  "trf" : trf,
  "xrf" : xrf,
  "w" : w,
  "h" : h,
}
with open('moscap3d.geo', 'w') as ofh:
  ofh.write('''\
// This option may be important for background mesh
//Mesh.CharacteristicLengthExtendFromBoundary=0; /* do not extend from boundary points */
//Mesh.Algorithm3D=1 /* 1 is Delaunay, Tetgen */
//Mesh.CharacteristicLengthMax = 1; /*maximum characteristic length */
//Mesh.CharacteristicLengthMin = 0; /*maximum characteristic length */
//Mesh.CharacteristicLengthFromCurvature = 1
//Mesh.CharacteristicLengthFromPoints = 1
//Mesh.CharacteristicLengthExtendFromBoundary=0;
//Geometry.ScalingFactor=1.0e-7;
//Mesh.CharacteristicLengthMax = 2.5e-5; /*maximum characteristic length */
''')
  ofh.write(geom.get_code())
  ofh.write("\n")

  ofh.write('''
Field[1] = Box;
Field[1].VIn = %(lrf)s;
Field[1].VOut = %(lcar)s;
Field[1].XMin = %(xrf)s;
Field[1].XMax = %(trf)s+%(xrf)s;
Field[1].YMin = -0.5*%(h)s;
Field[1].YMax = +0.5*%(h)s;
Field[1].ZMin = 0;
Field[1].ZMax = %(w)s;
Background Field = 1;
Mesh.CharacteristicLengthExtendFromBoundary = 1;
Mesh.CharacteristicLengthFromPoints = 1;
Mesh.CharacteristicLengthMax = %(lcar)s; /*maximum characteristic length */
''' % mydict)
#  ofh.write("Coherence;\n")

