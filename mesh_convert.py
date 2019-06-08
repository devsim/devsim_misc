
# read node, face, ele file and convert to gmsh


def read_nodes_from_tetgen(ifh):
    ncoordinates = None
    coordinates = []
    for line in ifh:
        line = line.strip()
        if line and line[0] == "#":
            continue
        elif not ncoordinates:
            ncoordinates = int(line.split()[0])
        else:
            coordinates.append(line)
    if ncoordinates != len(coordinates):
        raise RuntimeError('issue reading coordinates')
    return coordinates


def read_physical_names(ifh):
    nphysicalnames = None
    inphysicalnames = False
    physicalnames = []

    for line in ifh:
        line = line.strip()
        if not inphysicalnames:
            if line.find('$PhysicalNames') == 0:
                inphysicalnames = True
                continue
        elif line.find('$EndPhysicalNames') == 0:
            break
        else:
            if not nphysicalnames:
                nphysicalnames = int(line)
            else:
                physicalnames.append(line)
    return physicalnames


def read_nodes_from_gmsh(ifh):
    ncoordinates = None
    coordinates = []
    innodes = False

    for line in ifh:
        line = line.strip()

        if not innodes:
            if line.find('$Nodes') == 0:
                innodes = True
                continue
        elif line.find('$EndNodes') == 0:
            break
        elif not ncoordinates:
            ncoordinates = int(line)
        else:
            coordinates.append(line)

    if ncoordinates != len(coordinates):
        raise RuntimeError('issue reading coordinates')

    return coordinates


def read_elements_from_gmsh(ifh):
    nelements = None
    triangles = []
    tetrahedra = []
    inelements = False

    for line in ifh:
        line = line.strip()

        if not inelements:
            if line.find('$Elements') == 0:
                inelements = True
                continue
        elif line.find('$EndElements') == 0:
            break
        elif not nelements:
            nelements = int(line)
        else:
            data = line.split()
            skip = int(data[2])
            outdata = data[2+skip:]
            # put physical region at the end
            outdata.append(data[3])
            # plus the elementary id
            outdata.append(data[4])
            if data[1] == '2':
                triangles.append(outdata)
            elif data[1] == '4':
                tetrahedra.append(outdata)
            else:
                raise RuntimeError('Issue reading elements')
    return (triangles, tetrahedra)

# we only want the triangles on a marked boundary


def read_triangles_from_tetgen(ifh):
    ntriangles = None
    triangles = []
    for line in ifh:
        line = line.strip()
        if line and line[0] == "#":
            continue
        elif not ntriangles:
            ntriangles = int(line.split()[0])
        else:
            data = line.split()
            # we are in a group
            if data[-1] != '0':
                triangles.append(data[1:5])
    return triangles


def read_tetrahedra_from_tetgen(ifh):
    ntetrahedra = None
    tetrahedra = []
    for line in ifh:
        line = line.strip()
        if line and line[0] == "#":
            continue
        elif not ntetrahedra:
            ntetrahedra = int(line.split()[0])
        else:
            data = line.split()
            # we are in a group
            if data[-1] != '0':
                tetrahedra.append(data[1:6])
    return tetrahedra


def write_format_to_gmsh(ofh):
    ofh.write('''\
$MeshFormat
2.2 0 8
$EndMeshFormat
''')


def write_nodes_to_gmsh(ofh, coordinates):
    ofh.write('$Nodes\n%d\n' % len(coordinates))
    for coordinate in coordinates:
        ofh.write(coordinate + '\n')
    ofh.write('$EndNodes\n')


def write_elements_to_gmsh(ofh, triangles, tetrahedra):
    nelements = len(triangles) + len(tetrahedra)
    ofh.write('$Elements\n%d\n' % nelements)
    index = 1
    for triangle in triangles:
        ofh.write('%d 2 2 %s %s ' %
                  (index, str(triangle[-2]), str(triangle[-1])))
        ofh.write(' '.join(str(x) for x in triangle[0:3]))
        ofh.write('\n')
        index += 1
    for tetrahedron in tetrahedra:
        ofh.write('%d 4 2 %s %s ' %
                  (index, str(tetrahedron[-2]), str(tetrahedron[-1])))
        ofh.write(' '.join(str(x) for x in tetrahedron[0:4]))
        ofh.write('\n')
        index += 1
    ofh.write('$EndElements\n')


def write_physical_names_to_gmsh(ofh, physical_names):
    ofh.write('$PhysicalNames\n%d\n' % len(physical_names))
    for pname in physical_names:
        ofh.write(pname + '\n')
    ofh.write('$EndPhysicalNames\n')


def tetgen_to_gmsh(basename, gmshname, groupsname):
    with open(basename + '.node') as ifh:
        coordinates = read_nodes_from_tetgen(ifh)
    with open(basename + '.face') as ifh:
        triangles = read_triangles_from_tetgen(ifh)
    with open(basename + '.ele') as ifh:
        tetrahedra = read_tetrahedra_from_tetgen(ifh)
    if groupsname:
        with open(groupsname) as ifh:
            physical_names = read_physical_names(ifh)
    with open(gmshname, 'w') as ofh:
        write_format_to_gmsh(ofh)
        write_physical_names_to_gmsh(ofh, physical_names)
        write_nodes_to_gmsh(ofh, coordinates)
        write_elements_to_gmsh(ofh, triangles, tetrahedra)


def gmsh_to_tetgen(gmshname, basename, groupsname):
    with open(gmshname) as ifh:
        pnames = read_physical_names(ifh)
        if groupsname:
            with open(groupsname, 'w') as ofh:
                write_physical_names_to_gmsh(ofh, pnames)
        ifh.seek(0)
        coordinates = read_nodes_from_gmsh(ifh)
        with open(basename + '.node', 'w') as ofh:
            ofh.write('%d 3 0 0\n' % len(coordinates))
            for node in coordinates:
                ofh.write(node + '\n')
        ifh.seek(0)
        triangles, tetrahedra = read_elements_from_gmsh(ifh)
        with open(basename + '.face', 'w') as ofh:
            ofh.write('%d 1\n' % len(triangles))
            for triangle in triangles:
                ofh.write(' '.join(triangle))
                ofh.write('\n')
        with open(basename + '.ele', 'w') as ofh:
            ofh.write('%d 1\n' % len(tetrahedra))
            for tetrahedron in tetrahedra:
                ofh.write(' '.join(tetrahedron))
                ofh.write('\n')


def read_gmsh_info(gmshname):
    with open(gmshname) as ifh:
        pnames = read_physical_names(ifh)
        ifh.seek(0)
        coordinates = read_nodes_from_gmsh(ifh)
        ifh.seek(0)
        triangles, tetrahedra = read_elements_from_gmsh(ifh)
    return {
        'pnames': pnames,
        "coordinates": coordinates,
        "triangles": triangles,
        "tetrahedra": tetrahedra,
    }


# TODO: need to add elementary id in tetgen to gmsh conversion

# def gmsh_to_tetgen(gmshname, basename):

# basename='test.1'
#outname = 'tetgen.msh'

#gmsh_to_tetgen('test.msh', 'test.1')
#tetgen_to_gmsh('test.1', 'test1.msh')

if __name__ == "__main__":

    import argparse

    # TODO: really need to use Elementary ID instead of Physical ID in tetgen.  Since we can have regions which are not physically connected.
    # maybe this is not really an issue.
    parser = argparse.ArgumentParser(
        description='Convert between Gmsh and Tetgen format')
    parser.add_argument(
        '--gmsh',           help='the gmsh file for input/output', required=True)
    parser.add_argument(
        '--tetgen',         help='the basename for tetgen input/output', default=True)
    parser.add_argument(
        '--groups',         help='file to input/output the physical names in gmsh format', required=False)
    parser.add_argument('--gmsh_to_tetgen', help="convert gmsh to tetgen",
                        default=False, action='store_true')
    parser.add_argument('--tetgen_to_gmsh', help="convert tetgen to gmsh",
                        default=False, action='store_true')

    args = parser.parse_args()

    if args.gmsh_to_tetgen and args.tetgen_to_gmsh:
        raise RuntimeError("may choose only gmsh_to_tetgen or tetgen_to_gmsh")

    if args.tetgen_to_gmsh:
        if not args.groups:
            raise RuntimeError("no file to get group names")
        tetgen_to_gmsh(args.tetgen, args.gmsh, args.groups)
    elif args.gmsh_to_tetgen:
        gmsh_to_tetgen(args.gmsh, args.tetgen, args.groups)
    else:
        raise ("no conversion selected")
