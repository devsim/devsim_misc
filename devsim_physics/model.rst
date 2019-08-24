

Starting with electric field:

.. math::

  \texttt{ElectricField} &= - \nabla \texttt{Potential} \\
  \texttt{DisplacementField} &= \epsilon \texttt{ElectricField}


Intrinsic Charge

.. math::
  \nabla \cdot D = q \cdot \left( p - n + N_D\right)

.. math::
  n &= n_i \exp \left( \frac{q \Psi}{k T} \right) \\
  p &= n_i \exp \left( -\frac{q \Psi}{k T} \right)

.. math::
  p - n &=  n_i \left( \exp \left( -\frac{q \Psi}{k T} \right) - \exp \left( \frac{q \Psi}{k T} \right) \right) \\
        &=  n_i \left( \exp \left( -\frac{q \Psi}{k T} \right) - \exp \left( \frac{q \Psi}{k T} \right) \right) \\
        &=  - n_i \left( \exp \left( \frac{q \Psi}{k T} \right) - \exp \left( -\frac{q \Psi}{k T} \right) \right) \\
        &=  - 2 n_i \sinh \left( \frac{q \Psi}{k T} \right)

