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

from devsim.python_packages.simple_physics import *
from devsim.python_packages.ramp import *
import refinement2
import devsim
import math

devsim.set_parameter(name = "extended_solver", value=True)
devsim.set_parameter(name = "extended_model", value=True)
devsim.set_parameter(name = "extended_equation", value=True)

device = "mos2d"

import gmsh_mos2d_create
gmsh_mos2d_create.create(device=device, infile="gmsh_mos2d2.msh", outfile="gmsh_mos2d2_out.msh")

silicon_regions=("gate", "bulk")
oxide_regions=("oxide",)
regions = ("gate", "bulk", "oxide")
interfaces = ("bulk_oxide", "gate_oxide")

for i in regions:
    CreateSolution(device, i, "Potential")

for i in silicon_regions:
    SetSiliconParameters(device, i, 300)
    CreateSiliconPotentialOnly(device, i)

for i in oxide_regions:
    SetOxideParameters(device, i, 300)
    CreateOxidePotentialOnly(device, i, "log_damp")

### Set up contacts
contacts = get_contact_list(device=device)
for i in contacts:
    tmp = get_region_list(device=device, contact=i)
    r = tmp[0]
    print("%s %s" % (r, i))
    CreateSiliconPotentialOnlyContact(device, r, i)
    set_parameter(device=device, name=GetContactBiasName(i), value=0.0)

for i in interfaces:
    CreateSiliconOxideInterface(device, i)

solve(type="dc", absolute_error=1.0e-13, relative_error=1e-12, maximum_iterations=30)
solve(type="dc", absolute_error=1.0e-13, relative_error=1e-12, maximum_iterations=30)

for i in silicon_regions:
    CreateSolution(device, i, "Electrons")
    CreateSolution(device, i, "Holes")
    set_node_values(device=device, region=i, name="Electrons", init_from="IntrinsicElectrons")
    set_node_values(device=device, region=i, name="Holes",     init_from="IntrinsicHoles")
    CreateSiliconDriftDiffusion(device, i, "mu_n", "mu_p")

for c in contacts:
    tmp = get_region_list(device=device, contact=c)
    r = tmp[0]
    CreateSiliconDriftDiffusionAtContact(device, r, c)

solve(type="dc", absolute_error=1.0e30, relative_error=1e-5, maximum_iterations=30)


node_indexes = {r : refinement2.get_node_index(device=device, region=r) for r in regions}

def get_silicon_model_values(device, region):
    '''
    returns a model for refinement of silicon regions
    '''
    node_index = node_indexes[region]

    potential = get_node_model_values(device=device, region=region, name="Potential")
    test_model1 = [1 if abs(potential[x[0]]-potential[x[1]]) > 0.05 else 0 for x in node_index]

    electrons = get_node_model_values(device=device, region=region, name="Electrons")
    test_model2 = [1 if abs(math.log10(electrons[x[0]])-math.log10(electrons[x[1]])) > 1 else 0 for x in node_index]

    test_model = refinement2.max_merge_lists((test_model1, test_model2))

    return test_model

def get_oxide_model_values(device, region):
    '''
    returns a model for non-refinement
    '''
    test_model = [0.0] * len(get_edge_model_values(device=device, region=region, name="EdgeLength"))
    return test_model

#pre populate empty lists into dict
refinement_dict = {r : [] for r in regions}

def collectrefinements(device):
    global refinement_dict
    printAllCurrents(device)
    for r in silicon_regions:
        refinement_dict[r].append(get_silicon_model_values(device=device, region=r))
    for r in oxide_regions:
        refinement_dict[r].append(refinement2.get_oxide_model_values(device=device, region=r))

#TODO: use more increments for collection
rampbias(device, "gate",  0.5, 0.5, 0.001, 100, 1e-10, 1e30, collectrefinements)
rampbias(device, "drain", 0.5, 0.25, 0.001, 100, 1e-10, 1e30, collectrefinements)

with open('bgmesh2.pos', 'w') as ofh:
    refinement2.print_header(ofh)
    for r in silicon_regions:
        mlist = refinement2.max_merge_lists(refinement_dict[r])
        refinement2.refine_common(fh=ofh, device=device, region=r, model_values=mlist, mincl=1e-8, maxcl=1e8)
    for r in oxide_regions:
        mlist = refinement2.max_merge_lists(refinement_dict[r])
        refinement2.refine_common(fh=ofh, device=device, region=r, model_values=mlist, mincl=1e-8, maxcl=1e8)
    refinement2.print_footer(ofh)

write_devices(file="test2.dat", type="tecplot")

# test to see if the accumulation of all biases make sense
#refinement_dict['bulk'].append(refinement2.max_merge_lists(refinement_dict['bulk']))
#print("\n".join([str(x) for x in zip(*refinement_dict['bulk'])]))
# check to see if there are refinements for lower biases, but not later ones
#print("\n".join([str(x) for x in zip(*refinement_dict['bulk']) if (x[-1] != 0 and x[-2] == 0)]))
