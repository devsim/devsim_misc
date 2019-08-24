
Impedance Field Method
----------------------


Derivation
~~~~~~~~~~

The Impedance Field Method (IFM) is for performing a sensitivity analysis with respect to multiple perturbations :cite:`Branin:ieeect:1973`, :cite:`Bonani:ieeeted:1998`.

Starting with 

.. math::

   A x = b

where :math:`A` is the sensitivity matrix, and :math:`b` is a vector containing a vector of fully correlated perturbations.  The response is then

.. math::

    x = A^{-1} b

The disadvantage of this direct method is that one solve must be performed for each vector of source perturbations.

If we are interested in one output, we define an elementary vector :math:`e_i` that selects the output as:

.. math::

    x_i = e_i^T x

where a :math:`1` is placed in row :math:`i` corresponding to the desired output variable.

The problem to be solved is then

.. math::

    x_i = e_i^T A^{-1} b

We recast the problem in the form

.. math::

    x_i = y^T b

where :math:`y` is defined as

.. math:: :label: doteqn

    y^T = e_i^T A^{-1}

Then we can solve

.. math:: :label: aeqn

    A^T y = e_i

so that only one matrix factorization is required for a given simulation matrix and output.  Then :eq:`doteqn` is a dot product of :math:`y` with any number of source perturbations.

From a statistical perspective, then:

.. math::

    \langle x_i, x_i^* \rangle = y^T \langle b, b^* \rangle y

which can be shown to be:

.. math::

    \overline {x_i x_i^*} = \sum_j y_j^*  y_j \overline {b_j b_j^*} + \sum_j \sum_k 2 Re \overline {y_j b_j b_k^* y_k^*}

where indexes :math:`j` and :math:`k` select the appropriate row in :math:`y` corresponding to each perturbation.  The correlations :math:`b_j b_k^*` must be known in order to account for any correlations which may exist.


Selecting the output
~~~~~~~~~~~~~~~~~~~~

From :eq:`aeqn`, it was assumed that :math:`e_i` was an elementary vector with a one in the row corresponding to the desired output variable.  In principle, it can be any vector which calculates the desired output quantity.

If the output variable is a voltage, and a current is desired, it is possible to use a standard small signal analysis to get the output impedance of the device, and use that for conversion.  Equivalently, it may be possible to use the impedance field entry in the row corresponding to the output.

The scalar impedance field
~~~~~~~~~~~~~~~~~~~~~~~~~~

The impedance field couples a perturbation in an equation to the output.  For the electron continuity equation, the effect would be

.. math::

  I = \int G_s \cdot R \partial r

where :math:`G_s` is the scalar Green's function, :math:`R` is the recombination rate and the integration is performed over each volume in the mesh.

Considering the device equations at each node, it is necessary to consider the desired perturbation unit.

============== ==================  ============================
Equation       Unit                Perturbation Unit
============== ==================  ============================
:math:`F_\psi` :math:`V \cdot cm`  :math:`1 / cm^3`
:math:`F_n`    :math:`1/sec`       :math:`1 / (cm^3 \cdot sec)`
:math:`F_p`    :math:`1/sec`       :math:`1 / (cm^3 \cdot sec)`
============== ==================  ============================

The scalar impedance field for the Poisson equation is:

.. math::

    G_{\psi, i} = -\frac{\epsilon}{q \cdot vol} y_{\psi, i}

where :math:`y_{\psi, i}` is the entry in :math:`y` which corresponds to the Poisson equation for node :math:`i`.  The :math:`vol` is the volume of the node.  The other parameters are material parameters, and the sign is based on how the dopant terms are entered into the system matrix.

The electron and hole scalar impedance field are then

.. math::

    G_{n, i} = -\frac{1}{vol} y_{n, i}

    G_{p, i} = -\frac{1}{vol} y_{p, i}


Vector impedance field
~~~~~~~~~~~~~~~~~~~~~~

The vector impedance field, :math:`\overrightarrow G_v`, is used to calculate the device response to current density fluctuations in noise analysis.  It is required to consider the effects of dopant fluctuations on moblity and bandgap narrowing.

If :math:`\overrightarrow j` is a fluctuation in the current density, then

.. math::

  I = \frac{1}{q} \int G_s \nabla \cdot \overrightarrow j \, \partial r

Using Green's identities

.. math::

  \int \left( G \nabla \cdot \overrightarrow j + \overrightarrow j \cdot \nabla G \right) \partial r = \int G \overrightarrow j \cdot \partial s


then

.. math:: :label: ffgf

  I = \frac{1}{q} \left[ \int {\overrightarrow G_v} \cdot \overrightarrow j \partial r + \int G_s \overrightarrow j \partial s \right]


where

.. math::

  \overrightarrow G_v = - \nabla G_s


In the noise literature, :eq:`ffgf` is replaced with

.. math::

  I = \frac{1}{q} \int {\overrightarrow G_v} \cdot \overrightarrow j \partial r

using the argument that the surface integral vanishes.  For our purposes, it is unclear if the full form should :eq:`ffgf` should be retained.



Density Gradient
~~~~~~~~~~~~~~~~

To account for the Density Gradient, it is necessary to fully couple them into the system of equations being solved.

The Density Gradient equations are only dependent on :math:`n` and :math:`p`.  However, in our implementation, the quasi-Fermi definitions for :math:`n` and :math:`p` are employed.  This means that doping effects could enter through bandgap narrowing models.

Since  :math:`n` and :math:`p` are fundamental solution variables, and are therefore constant, it seems that the impedance field is not required from the DG equations.

Boundary Conditions
~~~~~~~~~~~~~~~~~~~

For the case of ohmic contacts, the equations for :math:`\psi`, :math:`n`, :math:`p` are replaced with other equations.  Therefore nodes at the ohmic contacts should not be considered in the impedance fields with respect to the bulk equations.

For perturbations with respect to the work function, the contact impedance fields would be needed since they enter directly into the potential equation.

If it is necessary to transform output voltage to current, the impedance field with respect to voltage fluctuations in the potential equation could be considered.



