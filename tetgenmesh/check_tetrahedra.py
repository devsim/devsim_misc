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

from devsim import *
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if False:
    set_parameter(name = "extended_solver", value=True)
    set_parameter(name = "extended_model", value=True)
    set_parameter(name = "extended_equation", value=True)

def get_center(ecoordinate):
    mymat = np.zeros((3, 3))
    myrhs = np.zeros((3,1))
    c0 = ecoordinate[0]
    for i in range(3):
        ci = ecoordinate[i+1]
        #print coordinate[ni] - coordinate[n0]
        #print mymat[i,:]
        v = ci - c0
        myrhs[i] = 0.5*np.dot(v, v.T)
        mymat[i,:] = v

    ### solving for the center of the tetrahedron
    ### https://en.wikipedia.org/wiki/Tetrahedron#Circumcenter
    center = np.linalg.solve(mymat, myrhs) + c0.T

    ### Calculate the radius of the tetrahedron
    if True:
        ci = ecoordinate[0]
        v = ci - center.T
        radius = np.linalg.norm(v)

    else:
        for i in range(4):
            ci = ecoordinate[i]
            v = ci - center.T
            #print(np.linalg.norm(v))
            radius = np.linalg.norm(v)
            print(radius)
            #print()

    return np.array(center).squeeze(), radius


def plot_tetrahedron(ax, xs, ys, zs, center, radius):
    #ax.set_aspect('equal')
    for i in range(4):
        for j in range(i+1, 4):
            ax.plot(
                (xs[i], xs[j]),
              (ys[i], ys[j]),
              (zs[i], zs[j]), 'b', linewidth=0.5)

    if False:
        for i in range(4):
            ax.plot(
                (xs[i], center[0]),
                  (ys[i], center[1]),
                  (zs[i], center[2]), 'k', linewidth=0.5)
    mid_x = center[0]
    mid_y = center[1]
    mid_z = center[2]
    max_range = radius*1.0

    if True:
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = mid_x + radius * np.outer(np.cos(u), np.sin(v))
        y = mid_y + radius * np.outer(np.sin(u), np.sin(v))
        z = mid_z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x, y, z, linewidth=0.05)

    #ax.set_xlim(mid_x - max_range, mid_x + max_range)
    #ax.set_ylim(mid_y - max_range, mid_y + max_range)
    #ax.set_zlim(mid_z - max_range, mid_z + max_range)


def get_element_coordinates(coordinate, element):
    c = [coordinate[element[i]] for i in range(4)]
    return c

def get_tet_volume(element_coordinates):
    v = [None]*3
    for i in range(3):
        v[i] = element_coordinates[i+1] - element_coordinates[0]
    tet_vol = np.abs(np.dot(np.cross(v[0], v[1]), v[2].T))/6.0
    return float(tet_vol[0].item())

def get_volume_subdivided(element_coordinates, center):
    fcenter = 0.0
    for i in range(4):
        c2 = np.copy(element_coordinates)
        c2[i] = center.T
        #print(c2)
        fcenter += get_tet_volume(c2)
    return fcenter



if __name__ == "__main__":
    device="test"
    region="bulk"
    load_devices(file="test.msh")

    elements=get_element_node_list(device=device, region=region)

    x=get_node_model_values(device=device, region=region, name="x")
    y=get_node_model_values(device=device, region=region, name="y")
    z=get_node_model_values(device=device, region=region, name="z")

    coordinate = np.matrix(list(zip(x, y, z)))

    #print coordinate[1]
    tetrahedron_volumes=[None]*len(elements)
    actual_volumes=[None]*len(elements)
    element_node_volumes = get_element_model_values(device=device, region=region, name="ElementNodeVolume")

    for tet_index, e in enumerate(elements):
        tet_vol = get_tet_volume(get_element_coordinates(coordinate, e))
        tetrahedron_volumes[tet_index] = tet_vol
        actual_vol = sum([q for q in element_node_volumes[6*tet_index:6*(tet_index+1)]])
        #actual_vol = sum([abs(q) for q in element_node_volumes[6*tet_index:6*(tet_index+1)]])
        actual_volumes[tet_index] = 2*actual_vol


    ratios = [actual_volumes[i] / tetrahedron_volumes[i] for i in range(len(actual_volumes))]
    #for i in range(len(actual_volumes)):
    #for i in range(6):
    #    print(i, actual_volumes[i], tetrahedron_volumes[i], ratios[i])

    bad_count = 0
    tolerance = 1. + 1e-2
    max_ratio = 0;
    mytet = None;
    bad_tets = []
    for i, ratio in enumerate(ratios):
        if ratio > max_ratio:
            max_ratio = ratio
            maxtet = i
        if ratio > tolerance:
            print(i, ratio)
            bad_count += 1
            bad_tets.append((i, ratio))

    print("bad_count %d / %d = %g%%" % (bad_count, len(ratios), (100.*bad_count)/len(ratios)))


    #print maxtet, max_ratio

    print("actual %g" % sum(actual_volumes))
    print("tetra  %g" % sum(tetrahedron_volumes))


    mytet = maxtet
    #mytet = 3579
    #mytet = 0


    #xs = []
    #ys = []
    #zs = []
    #for i in range(4):
    #    ni = elements[mytet][i]
    #    xs.append(x[ni])
    #    ys.append(y[ni])
    #    zs.append(z[ni])


    #exit()
    #print foo + coordinate[n0].T
    #exit()


    #print element_node_volumes[6*mytet:6*(mytet+1)]

    if False:
        i = 0
        c = get_element_coordinates(coordinate, elements[i])
        center, radius = get_center(c)
        print("%g actual" % actual_volumes[i])
        print("%g tetra" % tetrahedron_volumes[i])
        fcenter = get_volume_subdivided(c, center)
        print("%g fcenter" % fcenter)
        #raise RuntimeError("DEBUG")

    #print v[2]
        ax = plt.axes(projection='3d')

        #for j, r in bad_tets[0:10]:
        worst_tets = sorted(bad_tets, key=lambda x : x[1], reverse=True)[0:5]
        for j, r in worst_tets:
            xs = []
            ys = []
            zs = []
            for i in range(4):
                ni = elements[j][i]
                xs.append(x[ni])
                ys.append(y[ni])
                zs.append(z[ni])
            #center, radius = get_center(c)
            center, radius = get_center(get_element_coordinates(coordinate, elements[j]))
            print("%g actual" % actual_volumes[j])
            print("%g tetra" % tetrahedron_volumes[j])
            c = get_element_coordinates(coordinate, elements[j])
            fcenter = get_volume_subdivided(c, center)
            print("%g fcenter" % fcenter)
            #raise RuntimeError("DEBUG")
            plot_tetrahedron(ax, xs, ys, zs, center, radius)

        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_zlim(0,1)
        plt.show()

    import write_background
    points = []
    if True:
        for j, r in bad_tets:
            center, radius = get_center(get_element_coordinates(coordinate, elements[j]))
            c = [float(x) for x in center]
            points.append(c)
        write_background.write_nodes("bad.node", points)
        with open("test.1.node", 'r') as ifh:
            org = ifh.readlines()[1:-1]
        orgpoints = [[float(y) for y in x.split()[1:]] for x in org]
        orgpoints.extend(points)
        write_background.write_nodes("refine.node", orgpoints)
        #print(orgpoints)
    #print(points)

# debugging elementedgecouple based volume for maxtet
    maxtet = 0
    element_model(device=device, region=region, name='DerivedEdgeVolume', equation='1./6. * ElementEdgeCouple * EdgeLength')
    evol = get_element_model_values(device=device, region=region, name='DerivedEdgeVolume')
    print(evol[6*maxtet:6*maxtet+6])
    print(sum(evol[6*maxtet:6*maxtet+6]))
    print(element_node_volumes[6*maxtet:6*maxtet+6])
    print(sum(element_node_volumes[6*maxtet:6*maxtet+6]))
    print(actual_volumes[maxtet])
    print(tetrahedron_volumes[maxtet])

    print(coordinate)
    print(elements)
    print('start centers')
    for e in elements:
        center, radius = get_center(get_element_coordinates(coordinate, e))
        print(center)
