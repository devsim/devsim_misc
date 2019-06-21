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

def log_string(variable, minimum_value):
    '''
        equation for log10 of variable
    '''
    return "log(abs(%s) + %s)/log(10)" % (variable, str(minimum_value))

def signed_log_string(variable, minimum_value):
    '''
        signed log10 of variable
    '''
    return "sign(%s) * %s" % (variable, log_string(variable, minimum_value))

def scalar(variable, minimum_value):
    '''
        original variable value
    '''
    # consider incorporating signed value
    return variable

def diff_equation(name, bisection):
    '''
        model string to return 1 if criteria is met
    '''
    return "abs(%s@n0-%s@n1) > %s" % (name, name, str(bisection))

def create_models(device, region, name, variable, minimum_value, bisection, function):
    '''
        setup sequence of models
    '''
    node_model(device=device, region=region, name=name, equation=function(variable=variable, minimum_value=minimum_value))
    edge_from_node_model(device=device, region=region, node_model=name)
    edge_model(device=device, region=region, name=name+"_edge", equation=diff_equation(name, bisection))

def run(device, region, outfile, mincl, maxcl, pdiff):
    '''
        mincl: minimum characteristic length
        maxcl: maximum characteristic length
    '''

    # identify all edges that need to be bisected
    # ultimately translated to an element
    edge_from_node_model(node_model="node_index", device=device, region=region)

    # net doping signed log
    # include a minimum density
    # bisect if more than 4 order of magnitude difference
    create_models( device=device, region=region, name="SLNetDoping", variable="NetDoping", minimum_value=1, bisection=4, function=signed_log_string) 

    # potential difference
    # difference from interface

#    x = get_node_model_values(device=device, region=region, name="x")
#    y = get_node_model_values(device=device, region=region, name="y")
#
#    element_from_node_model(node_model="node_index",
#                            device=device, region=region)
#    en0 = get_element_model_values(
#        device=device, region=region, name='node_index@en0')
#    en1 = get_element_model_values(
#        device=device, region=region, name='node_index@en1')
#    en2 = get_element_model_values(
#        device=device, region=region, name='node_index@en2')
#
#    en0 = [int(x) for x in en0]
#    en1 = [int(x) for x in en1]
#    en2 = [int(x) for x in en2]
#
#    element_model(device=device, region=region,
#                  name="eindex", equation="edge_index")
#    eindex = get_element_model_values(
#        device=device, region=region, name='eindex')
#    eindex = [int(x) for x in eindex]
#
#    emag_refinement(device, region)
#    contact_refinement(device, region)
#    potential_refinement(device, region, pdiff)
#    #doping_refinement(device, region, ldiff)
#
#    #element_model(device=device, region=region, name="clen", equation="max(lognetdoping_norm, SA)")
#    #element_model(device=device, region=region, name="clen", equation="max(potential_norm, SA)")
#    element_model(device=device, region=region,
#                  name="clen", equation="max(max(Enorm, SA), potential_norm)")
#    cl = get_element_model_values(device=device, region=region, name='clen')
#
#    node_cl = [0.0]*len(x)
#    fh = open(outfile, 'w')
#    print('View "background mesh" {', file=fh)
#    for i in range(len(cl)//3):
#        j = i * 3
#        v = cl[j]
#        ni0 = en0[j]
#        ni1 = en1[j]
#        ni2 = en2[j]
#        # here we use mincl
#        if (v > 0):
#            node_cl[ni0] = mincl*v
#            node_cl[ni1] = mincl*v
#            node_cl[ni2] = mincl*v
#        else:
#            if node_cl[ni0] == 0.0:
#                node_cl[ni0] = maxcl
#            if node_cl[ni1] == 0.0:
#                node_cl[ni1] == maxcl
#            if node_cl[ni2] == 0.0:
#                node_cl[ni2] = maxcl
#
#    minx = 1e30
#    miny = 1e30
#    maxx = 0.0
#    maxy = 0.0
#    for i in range(len(cl)//3):
#        j = i * 3
#        ni0 = en0[j]
#        ni1 = en1[j]
#        ni2 = en2[j]
#        xp = (x[ni0], x[ni1], x[ni2])
#        yp = (y[ni0], y[ni1], y[ni2])
#        # if node_cl[ni0] and node_cl[ni1] and node_cl[ni2]:
#        print("ST(%g, %g, %g, %g, %g, %g, %g, %g, %g) {%g, %g, %g};" % (
#            xp[0], yp[0], 0.0,
#            xp[1], yp[1], 0.0,
#            xp[2], yp[2], 0.0,
#            node_cl[ni0], node_cl[ni1], node_cl[ni2]), file=fh)
#        if min(xp) < minx:
#            minx = min(xp)
#        elif max(xp) > maxx:
#            maxx = max(xp)
#        if min(yp) < miny:
#            miny = min(yp)
#        elif max(yp) > maxy:
#            maxy = max(yp)
#    print('};', file=fh)
#    fh.close()
#    print("BOX: %g %g %g %g" % (minx, miny, maxx, maxy))
#

