
Transient Method
----------------

.. need to confirm gamma values make sense from semiconductor simulation transient paper

See :cite:`bank1270142` for a description of the TRBDF2 method.

Integration
~~~~~~~~~~~

General Integration
^^^^^^^^^^^^^^^^^^^

.. math::

  0 = a_0 q_0 + a_1 q_1 + a_2 q_2 + b_0 i_0 + b_1 i_1 + b_2 i_2

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

Combination of 2 methods

.. math::

  \gamma &= 2 - \sqrt{2}

and use TR followed by BDF2

.. reference famous paper

Projection
~~~~~~~~~~

Calculate :math:`q_0` as part of the solution process.  Then compare with:

.. math::

  0 = i_1 + \frac{q_{proj} - q_1}{t_{\Delta}}

  q_{proj} = i_1 t_{\Delta} + q_1

Calculate error between projection and actual charge solution

