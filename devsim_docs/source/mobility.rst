
Mobility
--------

In its simplest form, mobility is a nodal quantity.  For current density calculations, the mobility needs to be calculated on the edge connecting two nodes.  Using an arithmetic average

.. math::

  \mu_{edge} = \frac{\mu_{{node}_0} + \mu_{{node}_1}}{2}

For the case of velocity saturation, mobility is dependent on the field parallel to current flow.


In addition, the electric field normal affects mobility components such as surface roughness, coulomb scattering, and acoustic phonon scattering.


Procedure

#. Nodal mobility components

#. Project onto Edge

#. Calculate Et on element edge

#. Calculate combined Element edge mobility

#. Apply Matthiessen's rule to get low field mobility

#. Calculate El on element edge

#. Apply velocity saturation to get high field mobility
