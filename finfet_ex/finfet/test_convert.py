

def find_interfaces(tetrahedra):
    set_dict = {}
    for t in tetrahedra:
        # physical number, elementary id
        pnum = (t[-2], t[-1])
        if pnum not in set_dict:
            set_dict[pnum] = set([])
        the_set = set_dict[pnum]
        n = sorted(t[0:4])
        tuples_to_add = [
            tuple([n[0], n[1], n[2]]),
          tuple([n[0], n[1], n[3]]),
          tuple([n[0], n[2], n[3]]),
          tuple([n[1], n[2], n[3]]),
        ]
        for u in tuples_to_add:
            if u in the_set:
                the_set.remove(u)
            else:
                the_set.add(u)
    pnums = sorted(set_dict.keys())
    boundaries = {}
    for i in range(len(pnums)):
        pnum_i = pnums[i]
        set1 = set_dict[pnum_i]
        for j in range(i+1, len(pnums)):
            pnum_j = pnums[j]
            # skip when elementary id matches
            if pnum_i[0] == pnum_j[0]:
                continue
            set2 = set_dict[pnum_j]
            intersection = set1.intersection(set2)
            if intersection:
                boundaries[(pnum_i, pnum_j)] = sorted(intersection)
    return boundaries

def delete_coordinates(coordinates, triangles, tetrahedra):
    cmap = [None] * (len(coordinates) + 1)
    vertices = set([])
    for t in triangles:
        vertices.update(t[0:3])
    for t in tetrahedra:
        vertices.update(t[0:4])
    vertices = sorted(vertices)

    for i, j in enumerate(vertices, 1):
        cmap[j] = i


    new_coordinates = [None] * len(vertices)
    for i, j in enumerate(vertices, 1):
        # this is a text string with the first digit being the enumeration
        c = coordinates[j-1].split()
        c[0] = str(i)
        new_coordinates[i-1] = " ".join(c)

    new_triangles = [None] * len(triangles)
    for i, t in enumerate(triangles):
        #print t
        nv = [cmap[x] for x in t[0:3]]
        nv.extend(t[-2:])
        #print nv
        new_triangles[i] = tuple(nv)

    new_tetrahedra = [None] * len(tetrahedra)
    for i, t in enumerate(tetrahedra):
        nv = [cmap[x] for x in t[0:4]]
        nv.extend(t[-2:])
        new_tetrahedra[i] = tuple(nv)

    return new_coordinates, new_triangles, new_tetrahedra

def get_next_elem_id(elem_ids):
    nid = max(elem_ids) + 1
    return nid

def get_next_phys_id(pname_map):
    nid = max(pname_map.keys()) + 1
    return nid

def delete_region_tetrahedra(pname_map, name, tetrahedra):
    for k, v in pname_map.items():
        if v[1] == name:
            dim = v[0]
            pnum = k
    if dim != 3:
        raise RuntimeError("Expecting %s to be a volume" % (name,))
    new_tetrahedra = [x for x in tetrahedra if x[-2] != pnum]
    return new_tetrahedra

def get_name(name0, name1, name_priority, interface_names):
    ret = None
    for i in interface_names:
        regions = i['regions']
        if name0 in regions and name1 in regions:
            ret = i['interface']
            break
    if ret:
        return ret
    if name0 in name_priority and name1 in name_priority:
        if name_priority.index(name0) < name_priority.index(name1):
            ret = "%s_%s" % (name0, name1)
        else:
            ret = "%s_%s" % (name1, name0)
    else:
        raise RuntimeError("No priority index for %s, %s" % (name0, name1))
    return ret

def process_tetrahedra(tetrahedra):
    '''
    converts input tetrahedra from strings to ints
    gets unique set of elementary ids
    '''
    int_tetrahedra = []
    elem_ids = set([])
    for t in tetrahedra:
        # process into ints
        ints = [int(x) for x in t]
        # read physical number
        if ints[-2] != 0:
            int_tetrahedra.append(ints[1:])
            elem_ids.add(ints[-1])
    return int_tetrahedra, elem_ids

def get_pname_map(gmsh_pnames):
    pname_map = {}
    for p in gmsh_pnames:
        data = p.split()
        dim = int(data[0])
        index = int(data[1])
        name = data[2][1:-1]
        #print name
        pname_map[index] = (dim, name)
    return pname_map

def get_interface_map(interfaces, pname_map, elem_ids, name_priority, interface_names):
    interface_map = {}
    # each new interface gets a new elementary id
    for i in sorted(interfaces.keys()):
        interface = interfaces[i]
        new_elem_id = get_next_elem_id(elem_ids)
        elem_ids.add(new_elem_id)

        name0 = pname_map[i[0][0]][1]
        name1 = pname_map[i[1][0]][1]

        new_name = get_name(name0, name1, name_priority, interface_names)
        if new_name not in interface_map:
            phys_id = get_next_phys_id(pname_map)
            pname_map[phys_id] = (2, new_name)
            interface_map[new_name] = {
                'phys_id' : phys_id,
              'elem_id' : {},
            }
        interface_map[new_name]['elem_id'][new_elem_id] = interface
    return interface_map

def get_surface_triangles(interface_map):
    triangles=[]
    for i in sorted(interface_map.keys()):
        phys_id = interface_map[i]['phys_id']
        print("%s %d" % (i, phys_id))
        for elem_id in sorted(interface_map[i]['elem_id'].keys()):
            itriangles = interface_map[i]['elem_id'][elem_id]
            print("  %d %d" % (elem_id, len(itriangles)))
            for t in itriangles:
                u = list(t)
                u.append(phys_id)
                u.append(elem_id)
                triangles.append(tuple(u))
    return triangles

def delete_regions(regions_to_delete, pname_map, coordinates, triangles, tetrahedra):
    '''
    delete tetrahedra from specified regions
    then remove unneeded coordinates
    '''
    new_tetrahedra = tetrahedra[:]
    for r in regions_to_delete:
        new_tetrahedra = delete_region_tetrahedra(pname_map, r, new_tetrahedra)

    (new_coordinates, new_triangles, new_tetrahedra) = delete_coordinates(coordinates, triangles, new_tetrahedra)

    return new_coordinates, new_triangles, new_tetrahedra

def scale_coordinates(coordinates, scale):
    new_coordinates = [None] * len(coordinates)
    for i, c in enumerate(coordinates):
        e = c.split()
        v = [scale*float(x) for x in e[1:]]
        new_coordinates[i] = e[0] + " " + " ".join(["%1.15g" % x for x in v])
    return new_coordinates

import yaml
def run(args):

    gmshinfo = mesh_convert.read_gmsh_info(args.input_mesh)

    with open(args.yaml) as f:
        yaml_map = yaml.safe_load(f)
    print(yaml_map)

    outfile = args.output_mesh

    tetrahedra, elem_ids = process_tetrahedra(gmshinfo['tetrahedra'])

    interfaces = find_interfaces(tetrahedra)

    #for i in sorted(interfaces.keys()):
    #  print(i, len(interfaces[i]))


    pname_map = get_pname_map(gmshinfo['pnames'])

    name_priority = yaml_map['name_priority']

    interface_names = yaml_map['interfaces']

    interface_map = get_interface_map(interfaces, pname_map, elem_ids, name_priority, interface_names)

    triangles = get_surface_triangles(interface_map)

    pnames = []
    for i in sorted(pname_map.keys()):
        x = '%d %d "%s"' % (pname_map[i][0], i, pname_map[i][1])
        print(x)
        pnames.append(x)

    #print(gmshinfo['pnames'])
    print(pnames)
    print(tetrahedra[0])
    print(triangles[0])

    print(len(tetrahedra))


    regions_to_delete = [x['contact'] for x in yaml_map['contact_regions'] if x['remove']]

    coordinates=gmshinfo["coordinates"]
    (coordinates, triangles, tetrahedra) = delete_regions(regions_to_delete, pname_map, coordinates, triangles, tetrahedra)

    scale = 1.0
    try:
        scale = yaml_map['options']['scale']
    except KeyError:
        pass


    if scale != 1.0:
        coordinates = scale_coordinates(coordinates, scale)



    with open(outfile, "w") as ofh:
        mesh_convert.write_format_to_gmsh(ofh)
        mesh_convert.write_physical_names_to_gmsh(ofh, pnames)
        mesh_convert.write_nodes_to_gmsh(ofh, coordinates)
        mesh_convert.write_elements_to_gmsh(ofh, triangles, tetrahedra)

    # TODO: write devsim_loader

import mesh_convert
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='remove contact volumes and add interfaces and contacts')
    parser.add_argument('--input_mesh', help="input mesh", required=True)
    parser.add_argument('--output_mesh', help="output mesh", required=True)
    parser.add_argument('--yaml', help="input mesh", required=True)
    args = parser.parse_args()
    run(args)

