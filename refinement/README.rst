
**WORK IN PROGRESS**

This work derives from the ``devsim_bjt_example`` project.

Work on strategy for refining meshes from Gmsh.  The starting point will be 2D and be extended to 3D later.

The ``.geo`` file is used to create an initial mesh.  An initial 2D mesh is created.  A simulation is performed.  A ``.pos`` format file is created based on the refinement criteria.  The ``.geo`` and ``.pos`` files are used to create a new mesh and the process is repeated.

The strategy will be:

.. code::
  gmsh -2 bjt.geo 
  python bjt_refine.py 
  gmsh -2 bjt.geo -bgm ./bjt_bgmesh.pos 
  python bjt_refine.py 
  gmsh -2 bjt.geo -bgm ./bjt_bgmesh.pos 
  python bjt_refine.py 
  gmsh -2 bjt.geo -bgm ./bjt_bgmesh.pos 
  python bjt_refine.py 
  gmsh -2 bjt.geo -bgm ./bjt_bgmesh.pos 
  python bjt_refine.py 





