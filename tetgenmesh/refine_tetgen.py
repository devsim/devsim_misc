
import load_tetgen
import check_tetrahedra
import numpy as np
import sys
import itertools
import math

def get_min_edge_length(ecoord):
    edge_lengths = []
    for i, j in (itertools.combinations((0,1,2,3),2)):
        edge_lengths.append(np.linalg.norm((ecoord[j]-ecoord[i])))
    return(min(edge_lengths))

if __name__ == "__main__":
    filebase = "test.1"
    raw_node = load_tetgen.read_file(filebase + '.node', load_tetgen.read_block)
    #raw_face = read_file(filebase + '.face', read_block)
    raw_ele  = load_tetgen.read_file(filebase + '.ele', load_tetgen.read_block)
    #print(raw_node)
    num_node = len(raw_node[1:])
    max_node = max([x[0] for x in raw_node])
    #print(max_node)
    coordinates = [None]*(max_node+1)
    for c in raw_node[1:]:
        ci = c[0]
        xi = c[1]
        yi = c[2]
        zi = c[3]
        coordinates[ci] = np.matrix((xi, yi, zi))

    #print(coordinates)
    elements = [x[1:5] for x in raw_ele[1:]]
    msize = [sys.float_info.max]*(max_node+1)
    tol = 1.0e-3
    bad_elements = []
    bad_count = 0
    total_tet_vol = 0.0
    total_sub_vol = 0.0
    for i, element in enumerate(elements):
        ecoord = check_tetrahedra.get_element_coordinates(coordinates, element)
        tet_vol = check_tetrahedra.get_tet_volume(ecoord)
        center, radius = check_tetrahedra.get_center(ecoord)
        sub_vol = check_tetrahedra.get_volume_subdivided(ecoord, center)
        ratio = sub_vol/tet_vol
        if ((ratio - 1.0) > tol):
            bad_count += 1
            bad_elements.append(i)
            #print("ratio %g %g %g" % (ratio, sub_vol, tet_vol))
        total_tet_vol += tet_vol
        total_sub_vol += sub_vol
    print("bad %d/%d %g%% vol %g %g" % (bad_count, len(elements), bad_count/len(elements) * 100., total_tet_vol, total_sub_vol))

    bad_element_map = set(bad_elements)
    for i, element in enumerate(elements):
        c = check_tetrahedra.get_element_coordinates(coordinates, element)
        mlength = get_min_edge_length(c)
        if i in bad_element_map:
            mlength *= 0.75
        for j in element:
            msize[j] = min(msize[j], mlength)
    with open(filebase + ".mtr", 'w') as ofh:
        ofh.write(("%d 1\n" % (num_node,)))
        for i, c in enumerate(coordinates):
            if c is None:
                continue
            ofh.write("%g\n" % (msize[i]))

