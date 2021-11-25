
.. _sec_transient:

Transient Method
----------------

.. need to confirm gamma values make sense from semiconductor simulation transient paper


Integration
~~~~~~~~~~~

General Integration
^^^^^^^^^^^^^^^^^^^

At each time step, the transient solver solves

.. math::

  0 = \boldsymbol{f}_0 = a_0 \boldsymbol{q}_0 + a_{-1} \boldsymbol{q}_{-1} + a_{-2} \boldsymbol{q}_{-2} + b_0 \boldsymbol{i}_0 + b_{-1} \boldsymbol{i}_{-1} + b_{-2} \boldsymbol{i}_{-2}

where :math:`\boldsymbol{f}_0` is the vector of net flux at each node in the mesh.  The :math:`\boldsymbol{i}_x` represents the time independent part of the semiconductor equations and :math:`\boldsymbol{q}_x` represents the time derivatives terms.  The subscript :math:`0` denotes the current time step being solved.  The subscripts :math:`-1` and :math:`-2` denote the previous two time steps.

At the beginning of each time step the components are copied in order so that:

.. math::

  \boldsymbol{i}_{-2} &= \boldsymbol{i}_{-1}

  \boldsymbol{i}_{-1} &= \boldsymbol{i}_{0}

  \boldsymbol{q}_{-2} &= \boldsymbol{q}_{-1}

  \boldsymbol{q}_{-1} &= \boldsymbol{q}_{0}



TRANSIENT_DC
^^^^^^^^^^^^

This is a steady state solution with:

.. math::

  a_0 &= 1

  a_1 &= 0

  b_0 &= 1

  b_1 &= 0

  b_2 &= 0

and represent the DC steady state.  This step can be used to initialize the initial time step so that the other transient methods can begin.


BDF1
^^^^

.. math::

  t_\Delta &= \gamma t_{step}

  t_f &= \frac{1}{t_\Delta}

  a_0 &= t_f

  a_1 &= -t_f

  b_0 &= 1

  b_1 &= 0

  b_2 &= 0

  \gamma &= 1


BDF2
^^^^

.. math::

  t_{\Delta} &= (1 - \gamma) t_{step}

  a_0       &= \frac{2 - \gamma}{t_{\Delta}}

  a_1       &= \frac{-1}{\gamma t_{\Delta}}

  a_2       &= \frac{1 - \gamma}{\gamma t_{step}}

  b_0       &= 1

  b_1       &= 0

  b_2       &= 0

  \gamma    &= 0.5

TR
^^

.. math::
  :label: TRMETHOD

  t_{\Delta} &= \gamma t_{step}

  t_{f}     &= \frac{2}{t_{\Delta}}

  a_0       &= t_{f}

  a_1       &= -t_{f}

  b_0       &= 1

  b_1       &= 1

  b_2       &= 0

TRBDF2
^^^^^^

Combination of 2 methods described in :cite:`bank1270142`.

.. math::

  \gamma &= 2 - \sqrt{2}

and use TR followed by BDF2


Projection
~~~~~~~~~~

Calculate :math:`\boldsymbol{q}_0` as part of the solution process.  Then compare with:

.. math::
  :label: transient_projection

  0 = i_1 + \frac{q_{proj} - q_1}{t_{\Delta}}

  q_{proj} = - i_1 t_{\Delta} + q_1

Calculate error between projection and actual charge solution

