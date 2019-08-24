
import pygmsh
from bool_common import *
geom = pygmsh.opencascade.Geometry(
  characteristic_length_min=.1,
  characteristic_length_max=2.5e-5
  )


h_top=40
corner_radius=4
half_device=False
lcar=1

z_fin=0
h_fin=25
w_fin=10
l_fin=100
x_fin=-0.5*l_fin
fin=create_fin_volume(geom, h=h_fin, w=w_fin, l=l_fin, x=x_fin, z=z_fin, cr=corner_radius, lcar=lcar, half_device=half_device)

z_ox=0
l_ox=50
t_ox=1
w_ox=w_fin+2*t_ox
h_ox=h_fin+t_ox
x_ox=x_fin + 0.5*(l_fin-l_ox)
oxide=create_fin_volume(geom, h=h_ox, w=w_ox, l=l_ox, x=x_ox, z=z_ox, cr=corner_radius, lcar=lcar, half_device=half_device)
oxide=geom.boolean_difference([oxide], [fin], delete_first=True, delete_other=False)

z_poly=0
l_poly=l_ox
t_poly=1
x_poly=0.5*(l_fin-l_poly)
w_poly=w_ox+2*t_poly
h_poly=h_ox+t_poly
x_poly=x_fin + 0.5*(l_fin-l_poly)
poly_volume=create_fin_volume(geom, h=h_poly, w=w_poly, l=l_poly, x=x_poly, z=z_poly, cr=corner_radius, lcar=lcar, half_device=half_device)
poly_volume=geom.boolean_difference([poly_volume], [oxide, fin], delete_first=True, delete_other=False)

l_box=l_fin
x_box = x_fin
w_box=2*w_poly
h_box = 5
z_box = -h_box
box_volume=create_box_volume(geom, h=h_box, w=w_box, l=l_box, x=x_box, z=z_box, lcar=lcar, half_device=half_device)

l_substrate = l_fin
x_substrate = x_fin
w_substrate = w_box
h_substrate=5
z_substrate = z_box - h_substrate
substrate_volume=create_box_volume(geom, h=h_substrate, w=w_substrate, l=l_substrate, x=x_substrate, z=z_substrate, lcar=lcar, half_device=half_device)

l_ground = l_fin
x_ground = x_fin
w_ground = w_box
h_ground = 1
z_ground = z_substrate - h_ground
ground_volume=create_box_volume(geom, h=h_ground, w=w_ground, l=l_ground, x=x_ground, z=z_ground, lcar=lcar, half_device=half_device)

l_drain = 12
w_drain = w_box
# Offset from the end of the device
x_drain = x_fin + 0
z_drain = 0
h_drain = h_top-z_drain
drain_volume=create_box_volume(geom, h=h_drain, w=w_drain, l=l_drain, x=x_drain, z=z_drain, lcar=lcar, half_device=half_device)
drain_volume=geom.boolean_difference([drain_volume], [poly_volume, oxide, fin], delete_first=True, delete_other=False)

l_source = 12
w_source = w_box
# Offset from the end of the device
x_source = x_fin + l_fin - l_source - 0
z_source = 0
h_source = h_top-z_source
source_volume=create_box_volume(geom, h=h_source, w=w_source, l=l_source, x=x_source, z=z_source, lcar=lcar, half_device=half_device)
source_volume=geom.boolean_difference([source_volume], [poly_volume, oxide, fin], delete_first=True, delete_other=False)

l_gate = 18
w_gate = w_box
x_gate = -0.5*l_gate
z_gate = 0
h_gate = h_top-z_gate
gate_volume=create_box_volume(geom, h=h_gate, w=w_gate, l=l_gate, x=x_gate, z=z_gate, lcar=lcar, half_device=half_device)
gate_volume=geom.boolean_difference([gate_volume], [poly_volume, oxide, fin], delete_first=True, delete_other=False)

l_air = l_box
w_air = w_box
x_air = x_box
z_air = 0
h_air = h_top
air_volume=create_box_volume(geom, h=h_air, w=w_air, l=l_air, x=x_air, z=z_air, lcar=lcar, half_device=half_device)
air_volume=geom.boolean_difference([air_volume], [poly_volume, oxide, fin, gate_volume, source_volume, drain_volume], delete_first=True, delete_other=False)

all_volumes = [air_volume, poly_volume, oxide, fin, box_volume, drain_volume, source_volume, gate_volume, substrate_volume, ground_volume]

geom.boolean_fragments( all_volumes,[], delete_first=True, delete_other=False)
#geom.add_physical_volume(air_volume, 'air')
geom.add_physical(poly_volume, 'poly')
geom.add_physical([oxide, air_volume], 'oxide')
geom.add_physical(fin, 'fin')
geom.add_physical(box_volume, 'box')
geom.add_physical(drain_volume, 'drain')
geom.add_physical(source_volume, 'source')
geom.add_physical(gate_volume, 'gate')
geom.add_physical(substrate_volume, 'substrate')
geom.add_physical(ground_volume, 'ground')

with open('fin.geo', 'w') as ofh:
  ofh.write('''\
// This option may be important for background mesh
Mesh.CharacteristicLengthExtendFromBoundary=0; /* do not extend from boundary points */
//Mesh.Algorithm3D=1 /* 1 is Delaunay, Tetgen */
//Mesh.CharacteristicLengthMax = 1; /*maximum characteristic length */
//Mesh.CharacteristicLengthMin = 0; /*maximum characteristic length */
//Mesh.CharacteristicLengthFromCurvature = 1
//Mesh.CharacteristicLengthFromPoints = 1
''')
  ofh.write(geom.get_code())
  ofh.write("\n")
#  ofh.write("Coherence;\n")

