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

devsim.set_parameter(name = "extended_solver", value=True)
devsim.set_parameter(name = "extended_model", value=True)
devsim.set_parameter(name = "extended_equation", value=True)

import gmsh_mos2d_create
device = "mos2d"
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

rampbias(device, "gate",  0.5, 0.5, 0.001, 100, 1e-10, 1e30, printAllCurrents)
rampbias(device, "drain", 0.5, 0.25, 0.001, 100, 1e-10, 1e30, printAllCurrents)

with open('bgmesh.pos', 'w') as ofh:
    refinement2.print_header(ofh)
    for r in silicon_regions:
        refinement2.refine_silicon_region(fh=ofh, device=device, region=r, mincl=1e-8, maxcl=1e8)
    for r in oxide_regions:
        refinement2.refine_oxide_region(fh=ofh, device=device, region=r, mincl=1e-8, maxcl=1e8)
    refinement2.print_footer(ofh)

write_devices(file="test.dat", type="tecplot")

