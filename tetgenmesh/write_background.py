
import numpy as np
#import io


def create_grid(p):
    nodes = []
    #p.extend((0.25, 0.5,9.5, 9.75))
    off = 0.5 * (p[1]-p[0])
    #p.extend((0.025, 0.05, 0.95, 0.975))
    p=sorted(p)

    #p = [0, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 1.0]
    #print(p)
    #print(len(p))
    index = 0
    for i in p:
        for j in p:
            for k in p:
                nodes.append((i,j,k))
    return nodes


def write_nodes(filename, nodes):
    with open(filename, 'w') as ofh:
        nnodes = len(nodes)
        ofh.write("%d 3 0 0\n" % (nnodes,))
        index = 0 
        for n in nodes:
                index +=1
                ofh.write("%d %g %g %g\n" % (index, *n))
                if False:
                    index +=1
                    ofh.write("%d %g %g %g\n" % (index, i+off, j+off, k+off))

def get_linspace():
    p = list(np.linspace(0,1, 11, dtype='d'))
    return p

if __name__ == "__main__":
    p = get_linspace()
    nodes = create_grid(p)
    write_nodes("test.a.node", nodes)

