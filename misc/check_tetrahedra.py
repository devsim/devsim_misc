# Copyright 2013 Devsim LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ds import *

create_gmsh_mesh(file="3dblock.msh", mesh="diode3d")
add_gmsh_region( mesh="diode3d" , gmsh_name="Bulk" , region="Bulk" , material="Silicon")
add_gmsh_contact( mesh="diode3d" , gmsh_name="Base" , region="Bulk" , name="top" , material="metal")
add_gmsh_contact( mesh="diode3d" , gmsh_name="Emitter" , region="Bulk" , name="bot" , material="metal")
finalize_mesh( mesh="diode3d")
create_device( mesh="diode3d" , device="resistor3d")
write_devices( file="gmsh_resistor3d_out.msh")

device="resistor3d"
region="Bulk"

elements=get_element_node_list(device=device, region=region)

x=get_node_model_values(device=device, region=region, name="x")
y=get_node_model_values(device=device, region=region, name="y")
z=get_node_model_values(device=device, region=region, name="z")

import numpy
coordinate = numpy.matrix(zip(x, y, z))

#print coordinate[1]
vol = 0.0
tetrahedron_volumes=[None]*len(elements)
actual_volumes=[None]*len(elements)
element_node_volumes = get_element_model_values(device=device, region=region, name="ElementNodeVolume")

for tet_index, e in enumerate(elements):
    v = [None]*3
    for i in range(3):
        v[i] = coordinate[e[i+1]] - coordinate[e[0]]
    tet_vol = numpy.abs(numpy.dot(numpy.cross(v[0], v[1]), v[2].T))/6.0
    vol += tet_vol
    actual_vol = sum([abs(q) for q in element_node_volumes[6*tet_index:6*(tet_index+1)]])
    actual_volumes[tet_index] = 2*actual_vol
    tetrahedron_volumes[tet_index] = float(tet_vol[0])


ratios = [actual_volumes[i] / tetrahedron_volumes[i] for i in range(len(actual_volumes))]
#for i in range(len(actual_volumes)):
for i in range(6):
    print i, actual_volumes[i], tetrahedron_volumes[i], ratios[i]

max_ratio = 0;
mytet = None;
for i, ratio in enumerate(ratios):
    if ratio > max_ratio:
        max_ratio = ratio
        maxtet = i
    if ratio > 1:
        print i, ratio

mytet = maxtet
mytet = 0

#print maxtet, max_ratio

print sum(actual_volumes)
print sum(tetrahedron_volumes)



mypoints=[]
xs = []
ys = []
zs = []
for i in range(4):
    ni = elements[mytet][i]
    xs.append(x[ni])
    ys.append(y[ni])
    zs.append(z[ni])

mymat = numpy.zeros((3, 3))
myrhs = numpy.zeros((3,1))
n0 = elements[mytet][0]
for i in range(3):
    ni = elements[mytet][i+1]
    #print coordinate[ni] - coordinate[n0]
    #print mymat[i,:]
    v = coordinate[ni] - coordinate[n0]
    myrhs[i] = 0.5*numpy.dot(v, v.T)
    mymat[i,:] = coordinate[ni] - coordinate[n0]

print mymat
print myrhs
foo = numpy.linalg.solve(mymat, myrhs) + coordinate[n0].T

for i in range(4):
    ni = elements[mytet][i]
    v = coordinate[ni] - foo.T
    print numpy.linalg.norm(v)
    radius = numpy.linalg.norm(v)
    print

#exit()
#print foo + coordinate[n0].T
#exit()

print mypoints

#print element_node_volumes[6*mytet:6*(mytet+1)]

#print v[2]
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()

ax = plt.axes(projection='3d')
ax.set_aspect('equal')
for i in range(4):
    for j in range(i+1, 4):
        ax.plot(
            (xs[i], xs[j]),
          (ys[i], ys[j]),
          (zs[i], zs[j]), 'b')

for i in range(4):
    ax.plot(
        (xs[i], foo[0]),
          (ys[i], foo[1]),
          (zs[i], foo[2]), 'k'
    )
mid_x = foo[0]
mid_y = foo[1]
mid_z = foo[2]
max_range = radius*1.0
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)


plt.show()

