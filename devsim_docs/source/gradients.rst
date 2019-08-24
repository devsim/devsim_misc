.. gradients documentation master file, created by
   sphinx-quickstart on Tue Jul 12 16:33:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Localized Gradient Models
=========================

.. Contents:

.. toctree::
   :maxdepth: 2



.. Indices and tables
.. ==================
.. 
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

Single Element
--------------

Electric Field
~~~~~~~~~~~~~~

Consider a vector field that we wish to ascribe to an edge or a node of a triangular or a tetrahedral element.  We begin by calculating the components along each element edge.  For the case of electric field, this is

.. math::
  E_{i,j} = \frac{\psi_i - \psi_j}{L_{i,j}}

where :math:`\psi_i` is the potential at node :math:`i`, and :math:`L_{i,j}` is the distance between the nodes :math:`i` and :math:`j`.

If the electric field on the element is known, this is equivalent to

.. math::
  E_{i,j} = \hat{s}_{i,j} \cdot \mathscr{E}

where :math:`\hat{s}_{i,j}` is the unit vector along the edge connecting nodes :math:`i` and :math:`j`.  For a tetrahedron with nodes :math:`(i,j,k,l)`, we can then use the components of the unit vectors to calculate


.. math::
  \begin{pmatrix}
    \hat{s}_{i,j}^{x} & \hat{s}_{i,j}^{y} & \hat{s}_{i,j}^{z} \\
    \hat{s}_{i,k}^{x} & \hat{s}_{i,k}^{y} & \hat{s}_{i,k}^{z} \\
    \hat{s}_{i,l}^{x} & \hat{s}_{i,l}^{y} & \hat{s}_{i,l}^{z} \\
  \end{pmatrix}
  \begin{pmatrix}
    \mathscr{E}_x \\ 
    \mathscr{E}_y \\ 
    \mathscr{E}_z
  \end{pmatrix}
  =
  \begin{pmatrix}
    E_{i,j} \\
    E_{i,k} \\
    E_{i,l}
  \end{pmatrix}

or

.. math::
  S_i \times \mathscr{E}
  =
  \begin{pmatrix}
    E_{i,j} \\
    E_{i,k} \\
    E_{i,l}
  \end{pmatrix}

The derivatives are then

.. math::
  \frac{\partial \mathscr{E}}{\partial \psi_i}
  =
  S_i^{-1} \times 
  \begin{pmatrix}
    \tfrac{\partial E_{i,j}}{\partial \psi_i} \\
    \tfrac{\partial E_{i,k}}{\partial \psi_i} \\
    \tfrac{\partial E_{i,l}}{\partial \psi_i}
  \end{pmatrix}

.. math::
  \frac{\partial \mathscr{E}}{\partial \psi_j}
  =
  S_i^{-1} \times 
  \begin{pmatrix}
    \tfrac{\partial E_{i,j}}{\partial \psi_j} \\
    0 \\
    0
  \end{pmatrix}

.. math::
  \frac{\partial \mathscr{E}}{\partial \psi_k}
  =
  S_i^{-1} \times 
  \begin{pmatrix}
    0 \\
    \tfrac{\partial E_{i,k}}{\partial \psi_k} \\
    0
  \end{pmatrix}

.. math::
  \frac{\partial \mathscr{E}}{\partial \psi_l}
  =
  S_i^{-1} \times 
  \begin{pmatrix}
    0 \\
    0 \\
    \tfrac{\partial E_{i,l}}{\partial \psi_l}
  \end{pmatrix}

by storing these :math:`S^{-1}` matrices, the electric field on each element and their derivatives may be stored.  It can be shown that since

.. math::
  E_{i,l} L_{i,l} = E_{i,j} L_{i,j} + E_{j,k} L_{j,k} + E_{k,l} L_{k,l}

that only one :math:`S` matrix would need to be formed for each tetrahedral element in the mesh.

Current Direction
~~~~~~~~~~~~~~~~~

What is needed
^^^^^^^^^^^^^^

What is ultimately needed is the unit vector, :math:`j`, which corresponds to the direction of current flow.

Since the current depends on the mobility, which depends on the current flow creates a cyclic dependency.  Laux suggests breaking this cycle by

1. Calculating the current directions based on constant mobility
2. Calculating the electric field based on the the constant mobility current
3. Calculating the final current based on the electric field dependent mobility


Using edge currents
^^^^^^^^^^^^^^^^^^^

If we wanted to apply the same treatment for electron or hole current, we would then calculate the current components, by using 2 matrices for each edge to calculate the current.  For the edge connecting nodes :math:`i` and :math:`j`, this would be


.. math::
  S_i \times J_i
  =
  \begin{pmatrix}
    J_{i,j} \\
    J_{i,k} \\
    J_{i,l}
  \end{pmatrix}

and

.. math::
  S_j \times J_j
  =
  \begin{pmatrix}
    J_{j,i} \\
    J_{j,k} \\
    J_{j,l}
  \end{pmatrix}

and these could be weighted as

.. math::
  J = {0.5 J_i + 0.5 J_j}

Where the equal weighting is chosen for its relative ease of implementation.  For a 2D implementation, the weighting of the triangle edges has been done by Laux based on the area of the perpendicular bisectors of the edges off of nodes :math:`i` and :math:`j`.  In principle, this could be


.. math::
  J = \frac{\left(d_{i,k} + d_{i,l}\right) J_i + \left(d_{j,k} + d_{j,l}\right) J_j}{d_{i,k} + d_{i,l} + d_{j,k} + d_{j,l}}


Derivatives with respect to nodal quantities would then be done using the chain rule using a similar approach as shown for the electric field.

Using nearest interface
~~~~~~~~~~~~~~~~~~~~~~~

A more stable way of evaluating the mobility is to base the current directions based on the nearest interface.  It is considered stable since the current directions are not iteration dependent.

To do this, a line is drawn from center of the edge to the nearest interface.  The plane formed at the interface node is considered to be the direction parallel to current flow.  The direction perpendicular to current flow is then the line normal to the plane.


Averaging the elements
----------------------

Calculating electric field components
-------------------------------------

.. discuss surface roughness in light of the DG model and that carriers are not likely to be at the interface
