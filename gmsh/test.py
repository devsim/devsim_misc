from devsim import *
mesh="mymesh"
device="mydevice"

create_gmsh_mesh(mesh=mesh, file='test.msh')
add_gmsh_region  (mesh=mesh, gmsh_name="bulk",    region="bulk", material="Silicon")
add_gmsh_region  (mesh=mesh, gmsh_name="disk",    region="disk", material="Silicon")
add_gmsh_region  (mesh=mesh, gmsh_name="nlayer",    region="nlayer", material="Silicon")
add_gmsh_contact (mesh=mesh, gmsh_name="top",    region="disk", material="metal", name="top")
add_gmsh_contact (mesh=mesh, gmsh_name="bot",    region="nlayer", material="metal", name="bot")
add_gmsh_interface (mesh=mesh, gmsh_name="disk_bulk", region0="disk", region1="bulk", name="disk_bulk")
add_gmsh_interface (mesh=mesh, gmsh_name="bulk_nlayer", region0="bulk", region1="nlayer", name="bulk_nlayer")
finalize_mesh    (mesh=mesh)
create_device    (mesh=mesh, device=device)

