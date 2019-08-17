# Copyright 2016 Devsim LLC
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
import sys
import math

#def log_string(variable, minimum_value):
#    '''
#        equation for log10 of variable
#    '''
#    return "log(abs(%s) + %s)/log(10)" % (variable, str(minimum_value))
#
#def signed_log_string(variable, minimum_value):
#    '''
#        signed log10 of variable
#    '''
#    return "sign(%s) * %s" % (variable, log_string(variable, minimum_value))
#
#def scalar(variable, minimum_value):
#    '''
#        original variable value
#    '''
#    # consider incorporating signed value
#    return variable
#
#def diff_equation(name, bisection):
#    '''
#        model string to return 1 if criteria is met
#    '''
#    return "abs(%s@n0-%s@n1) > %s" % (name, name, str(bisection))
#
#def create_models(device, region, name, variable, minimum_value, bisection, function):
#    '''
#        setup sequence of models
#    '''
#    node_model(device=device, region=region, name=name, equation=function(variable=variable, minimum_value=minimum_value))
#    edge_from_node_model(device=device, region=region, node_model=name)
#    edge_model(device=device, region=region, name=name+"_edge", equation=diff_equation(name, bisection))

def print_header(fh):
    fh.write('View "background mesh" {\n')

def print_footer(fh):
    fh.write('};\n')

def get_edge_index(device, region):
    '''
maps element edges to regular edges
'''
    # now iterate over the edges of the element
    element_model(device=device, region=region,
                  name="eindex", equation="edge_index")
    eindex = get_element_model_values(
        device=device, region=region, name='eindex')
    eindex = [int(x) for x in eindex]
    return eindex

def get_node_index(device, region):
    '''
maps head and tail nodes of from their edge index
'''
    # identify all edges that need to be bisected
    # ultimately translated to an element
    edge_from_node_model(node_model="node_index", device=device, region=region)
    nindex = list(
      zip(
        [int(x) for x in get_edge_model_values(device=device, region=region, name="node_index@n0")],
        [int(x) for x in get_edge_model_values(device=device, region=region, name="node_index@n1")],
      )
    )
    return nindex

def calculate_clengths(device, region, model_values):
    '''
    calculate the characteristic lengths for each edge by bisecting the edge length
'''
    edge_lengths = get_edge_model_values(device=device, region=region, name="EdgeLength")
    bisection_count = 0
    clengths = [None] * len(edge_lengths)
    for i, v in enumerate(model_values):
      if v != 0:
        clengths[i] = 0.5 * edge_lengths[i]
        bisection_count += 1
      else:
        clengths[i] = edge_lengths[i]
    print("Bisections: %d" % bisection_count)
    return clengths


def get_output_elements(nindex, eindex, clengths):
    '''
    gets the node indexes and the characterisic lengths for each element
'''
    # break into a per element basis
    outputelements = []
    for i in range(0, len(eindex), 3):
      ndict = {}
      for j in eindex[i:i+3]:
        v = clengths[j]
        for k in nindex[j]:
          if k in ndict:
            ndict[k] = min(ndict[k], v)
          else:
            ndict[k] = v
      outputelements.append(ndict)
      #print(ndict)
    return outputelements

def get_output_elements2(nindex, eindex, clengths):
    '''
    gets the node indexes and the characterisic lengths for each element
'''
    # break into a per element basis
    outputelements = []
    for i in range(0, len(eindex), 3):
      ndict = {}
      mv = clengths[eindex[i]]
      for j in eindex[i+1:i+3]:
        mv = min(mv, clengths[j])
      for j in eindex[i:i+3]:
        for k in nindex[j]:
          ndict[k] = mv
      outputelements.append(ndict)
      #print(ndict)
    return outputelements

def get_output_elements3(nindex, eindex, clengths):
    '''
    gets the node indexes and the characterisic lengths for each element
'''
    node_map = {}
    # get node indexes for each edge
    for i, n in enumerate(nindex):
        v = max(clengths[i], 1e-8)
        for ni in n:
            if ni not in node_map:
                node_map[ni] = v
            else:
                node_map[ni] = min(node_map[ni], v) 

    #break into a per element basis
    outputelements = []
    for i in range(0, len(eindex), 3):
        ndict = {}
        # mapping of element edge into an edge index
        for j in eindex[i:i+3]:
            # mapping of edge index into a node index
            for k in nindex[j]:
                if k not in ndict:
                    ndict[k] = node_map[k]
        outputelements.append(ndict)
    return outputelements

def print_elements(fh, device, region, elements):
    x = get_node_model_values(device=device, region=region, name="x")
    y = get_node_model_values(device=device, region=region, name="y")

    for e in elements:
      coords = []
      values = []
      for n, v in e.items():
        coords.extend((x[n], y[n], 0.0))
        values.append(v)
      coordstring = ", ".join([format(x, "1.15g") for x in coords])
      valuestring = ", ".join([format(x, "1.15g") for x in values])
      fh.write("ST(%s) {%s};\n" % (coordstring, valuestring))

def refine_common(fh, device, region, model_values):
    clengths = calculate_clengths(device=device, region=region, model_values=model_values)
  
    eindex = get_edge_index(device, region)
    nindex = get_node_index(device, region)


    outputelements = get_output_elements3(nindex=nindex, eindex=eindex, clengths = clengths)
    print_elements(fh=fh, device=device, region=region, elements=outputelements)

def refine_oxide_region(fh, device, region):
    '''
    '''
    # apply no refinement
    test_model = [0.0] * len(get_edge_model_values(device=device, region=region, name="EdgeLength"))

    refine_common(fh=fh, device=device, region=region, model_values=test_model)

def refine_silicon_region(fh, device, region):
    '''
    '''

    node_index = get_node_index(device=device, region=region)
    potential = get_node_model_values(device=device, region=region, name="Potential")
    test_model1 = [1 if abs(potential[x[0]]-potential[x[1]]) > 0.010 else 0 for x in node_index]

    electrons = get_node_model_values(device=device, region=region, name="Electrons")
    test_model2 = [1 if abs(math.log10(electrons[x[0]])-math.log10(electrons[x[1]])) > 1 else 0 for x in node_index]

    test_model = [max(x) for x in zip(test_model1, test_model2)]
    #test_model = test_model1

    #node_model(device=device, region=region, name="logElectrons", equation="log(Electrons)/log(10)")
    #edge_from_node_model(device=device, region=region, node_model='logElectrons')
    #edge_model(device=device, region=region, name="edgeLogElectrons", equation="abs(logElectrons@n0-logElectrons@n1)")
    ## test if the difference more than 1 order of magnitude
    #test_model1 = [1 if x > 2 else 0 for x in get_edge_model_values(device=device, region=region, name="edgeLogElectrons")]

    # test if the electric field in silicon is greater than 1e5
    #test_model2 = [1 if abs(x) > 1e4 else 0 for x in get_edge_model_values(device=device, region=region, name="ElectricField")]
    #test_model = [max(x) for x in zip(test_model1, test_model2)]
    #test_model = test_model1

    refine_common(fh=fh, device=device, region=region, model_values=test_model)



