
**WORK IN PROGRESS**

Work on strategy for refining MOS meshes from Gmsh.  The starting point will be 2D and be extended to 3D later.

MOS refinement strategy.  Based on logarithmic Electron density differences and Potential differences in the transistor.

This work derives from the ``devsim_bjt_example`` project.  However it is improved because it creates a background mesh to bisect elements that meet a criteria across their edges.


The ``.geo`` file is used to create an initial mesh.  An initial 2D mesh is created.  A simulation is performed.  A ``.pos`` format file is created based on the refinement criteria.  The ``.geo`` and ``.pos`` files are used to create a new mesh and the process is repeated.

Please see ``run.sh`` for a running example.  Both Gmsh and DEVSIM should be setup in your path.  By saving the output log for each run, you will see the number of Bisections decrease.

**FUTURE WORK**

This only collects data from the last bias point before the refinement2 module is called.  It would be interesting to adapt the script to sample the bisection criteria over several biases and merge them at the end to create the background mesh.

``mos2d_refine.py`` is refinement based on the last bias
``mos2d_refine2.py`` is refinement based on the all biases

