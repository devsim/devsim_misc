
def remove_comment(line_string):
    '''
    removes comment from string
    '''
    pos = line_string.find('#')
    return line_string[0:pos]

def read_block(ifh):
    lines = []
    for line in ifh:
        mline = remove_comment(line)
        msplit = mline.split()
        if not msplit:
            continue
        entries = [None] * len(msplit)
        for i, m in enumerate(msplit):
            try:
                entries[i] = int(m)
                continue
            except ValueError:
                pass
            entries[i] = float(m)
            continue

        lines.append(entries)
    return lines

def read_file(filename, func):
    '''
    read filename
    '''
    with open(filename, 'r') as ifh:
        return func(ifh)

def process_coordinate(node_block):
    data = node_block[1:]
    header = node_block[0]
    # This is the map between indexes to normalized indexes
    cmap = [None]*(max(data)[0]+1)
    num_nodes = header[0]
    coord = [None]*num_nodes
    for i, c in enumerate(data):
        coord[i] = [float(x) for x in c[1:]]
        cmap[c[0]] = i
    return cmap, coord

def process_elements(cmap, facet_block, num_nodes, attribute_index):
    element_map = {}
    for element in facet_block[1:]:
        region = element[attribute_index]
        element = [cmap[x] for x in element[1:num_nodes+1]]
        if region not in element_map:
            element_map[region] = []
        element_map[region].append(element)
    return element_map


if __name__ == "__main__":
    filebase = "test.1"


    raw_node = read_file(filebase + '.node', read_block)
    raw_face = read_file(filebase + '.face', read_block)
    raw_ele  = read_file(filebase + '.ele', read_block)

    cmap, coord = process_coordinate(raw_node)

    names_2d = {
      0 : None,
      1 : "top",
      2 : "bot",
    }

    names_3d = {
      0 : None,
      1 : "bulk"
    }

    triangles = process_elements(cmap, raw_face, 3, 4)
    #print(triangles)
    tetrahedra = process_elements(cmap, raw_ele, 4, 5)
    #print(tetrahedra)

    ### TODO: generalize
    physical_names = []
    physical_map = {}

    for n in (names_2d, names_3d):
        for k, v in n.items():
            if v:
                physical_map[v] = len(physical_names)
                physical_names.append(v)

    print(physical_names)

    coordinates = []
    for c in coord:
        coordinates.extend(c)
    coordinates = [0.06*x for x in coordinates]

    #print(coordinates)

    elements = []
    #print(triangles)
    for shapes, name_map in ((triangles, names_2d), (tetrahedra, names_3d)):
        for region_id, element in shapes.items():
            region_name = name_map[region_id]
            if not region_name:
                continue
            physical_id = physical_map[region_name]
            element_type = None
            if len(element[0]) == 3:
                element_type = 2
            elif len(element[0]) == 4:
                element_type =3
            else:
                raise RuntimeError("bad element")

            for shape in element:
                elements.extend((element_type, physical_id))
                elements.extend(shape)

    #print(elements)


    from devsim import *
    create_gmsh_mesh(mesh="test", coordinates=coordinates, elements=elements, physical_names=physical_names)
    add_gmsh_region(mesh="test", gmsh_name="bulk", region="bulk", material="silicon")
    add_gmsh_contact(mesh="test", gmsh_name="top", region="bulk", name="top", material="metal")
    add_gmsh_contact(mesh="test", gmsh_name="bot", region="bulk", name="bot", material="metal")
    finalize_mesh(mesh="test")
    create_device(mesh="test", device="test")
    write_devices(device="test", file="test.msh")
    write_devices(device="test", file="test.tec", type="tecplot")

    #0 node
    #1 edge
    #2 triangle
    #3 tetrahedron


    #physical_names = []
    #physical_map = {}
    #
    #for i in names_2d:
    #    
    #
    #
    #elements = []
    #for i in triangles:
    #
