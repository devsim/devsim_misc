
Adds interfaces to a 2D or 3D structure created with Gmsh.  See ``run.sh`` for running an example structure.

An optional yaml file can be used to configure additional behavior.
Please see ``ring.yaml`` for an example.

Recommended usage:

Create a .geo file with physical groups labeling volumes and surfaces.  The surfaces should denote contact boundary conditions.  Running the script will add interfaces.  It will also ensure that the interfaces do not share vertices with any other interfaces or contacts.

The input mesh must be created with the older Gmsh format:

::

  gmsh -2 -format 'msh2' gmsh_mos2d.geo


::

  python test_convert.py  --input_mesh gmsh_mos2d.msh  --output_mesh foo.msh 

The mesh can then be loaded in devsim for simulation.

The user should look in the updated msh file for the names:

::

  $PhysicalNames
  9
  1 1 "gate_contact"
  1 2 "gate_oxide_interface"
  1 4 "source_contact"
  1 5 "drain_contact"
  1 6 "body_contact"
  2 7 "gate"
  2 8 "oxide"
  2 9 "bulk"
  $EndPhysicalNames

where the 1st column is the dimension of the physical group, and the last column is its name when loaded into devsim.




  
