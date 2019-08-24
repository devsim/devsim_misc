Regions
-------

Entities
~~~~~~~~

* Device
* Region
* Interface
* Contact

Device contains Regions, Interfaces, Contacts

Circuit contains nodes attached to contacts and circuit elements.

The whole system contains all devices and circuit

Each contact is associated with 1 Region and possibly a circuit node.

Each interface is associated with 2 Regions


Assembly
~~~~~~~~

Coordinates
^^^^^^^^^^^

Coordinates are global to the entire structure.  They are essentially positions, and may be shared across multiple regions.

Nodes
^^^^^

Each region contains a list of nodes.  These nodes are uniquely numbered and are associated with an underlying coordinate.  Coordinates may be shared by different regions, however the node is distinct to the region.  An interface governs how the equations at these coincident nodes interact. 

Equation numbering
^^^^^^^^^^^^^^^^^^

Each equation is assigned a unique number for each node in a region.  The net flux of each equation is assembled into a sub matrix and RHS whose rows correspond to all of the interacting region nodes.

Permutation Vector
^^^^^^^^^^^^^^^^^^

The permutation vector is used to manipulate the assembly of equations in the Jacobian matrix.  If a contact boundary condition exists for an equation, the permutation entry for that node is set to -1, which means it is not loaded into the matrix.  (The contact equation assembly routine will separately load the current density into the circuit nodes.)

For the "Type 1" interface boundary condition described below, the equation number entry for region 2 permutes into the equation number entry for region 1.

Final Assembly
^^^^^^^^^^^^^^

Region Assembly
+++++++++++++++

A sub matrix and RHS is evaluated for each node in a region.  The permutation vector is used to avoid loading the bulk equation into the contact nodes.  For "Type 1" interfaces, the bulk equation for the 2nd region at an interface is permuted into the equation row for the first region.

For most cases, it is not necessary for the region equation assembly to explicitly handle whether or not an interface or contact node is being assembled.  These submatrix entries will be filtered out if they are not needed.

Interface Assembly
++++++++++++++++++

For the interface assembly, the permutation vector is ignored.  Flux contributions across the interface has already been handled in the Region Assembly.

For interface equations, there are two types of boundary conditions.

Type 1
______

The bulk flux equation for Region 1 and Region 2 are assembled into the row corresponding to Region 1.  An interface node model equation is evaluated and place into the row corresponding to Region 2.

This would be the natural boundary condition for the Poisson equation, as the interface model equation would enforce a continuous potential.

An example for this case would be having a continuous quasi-Fermi level between two similar material regions.

Type 2
______

The bulk flux equation for Region 1 and Region 2 are assembled into the rows corresponding to their respective regions.  An additional interface node model is added to the flux for Region 1 and subtracted from Region 2.  This additional flux term is integrated with respect to surface area of the interface between the nodes.

An example for this case would be tunneling at a heterojunction interface.

Contact Assembly
++++++++++++++++

Contact assembly ignores the permutation vector.  The contributions from the bulk equations are ignored during the Region assembly process.

The contact flux equation is then assembled in the bulk equation's place.   In the presence of an external circuit on the contact, the equation for the external current flux and charge displacement  is assembled into the circuit node equation.  This is integration is with respect to the surface area of the contact node.

Caveats
~~~~~~~

Interface conflicts
^^^^^^^^^^^^^^^^^^^

It is entirely possible to have multiple regions to share a node or edge.  In order to prevent issues with the equation assembly, it is important to make sure that these regions do not have conflicting permutations.

By definition, intersecting interfaces do not share surface area.  If you have 3 regions:

#. interface 1: r1 r2
#. interface 2: r1 r3

Note that this should not occur

#. interface 3: r2 r3 (does not exist)

If the abutting interfaces are all "Type 1", you just need to ensure that the first region for both interfaces is the same.   The permutation vector will then permute the bulk equations for the other regions into the bulk equation for the first region.  The constraint equation for each interface will then properly handle the relationship between the connected regions.

This may be attained by prioritizing the interfaces, so they are always treated in the same order.  Similarly for a mixture of "Type 1" and "Type 2" interfaces, it seems that this approach would work as well.

Contact conflicts
^^^^^^^^^^^^^^^^^

Overlapping contacts must be avoided.  This is since the current coming out of overlapping nodes would be double counted.  Contacts overlapping interfaces should be similarly avoided.  The permutation vector could either get corrupted, or current could be double counted as going out of the contact, and across the interface.

Circuit Equations
^^^^^^^^^^^^^^^^^

For a single device solution, equation numbers for the terminal currents are not necessary.  They are recovered after the dc solution has been obtained.  For time dependent simulation, the circuit equations are important to sum up the particle and displacement current.  They would also be important for small signal and impedance field simulation.

