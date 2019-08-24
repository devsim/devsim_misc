Density Gradient Method
-----------------------

DG Equation Discretization
~~~~~~~~~~~~~~~~~~~~~~~~~~

The density gradient equations to be solved are of the following form:

.. math::

  \Lambda_e = -b_n\frac{\nabla^2 \sqrt{n}}{\sqrt{n}}

  \Lambda_h = -b_p\frac{\nabla^2 \sqrt{p}}{\sqrt{p}}

where :math:`b_n`, :math:`b_p` are coefficients relating the gradient in :math:`\sqrt{n}` with a quantum correction.

 .. math::
 
   b_n = \frac{\gamma_n\hbar^2}{6 m_n}

   b_p = \frac{\gamma_p\hbar^2}{6 m_p}

Using:

.. math::

  \frac{\nabla^2 \sqrt{n}}{\sqrt{n}} = \frac{1}{2} \left\{\nabla^2 \log n + \frac{1}{2} \left(\nabla \log n\right)^2\right\}

and

.. math::

  \Phi_e = \log n

  \Phi_h = \log p

The equations become:

.. math::

  \Lambda_e + \frac{b_n}{2} \left( \nabla \cdot \nabla \Phi_e + \frac{1}{2} \left( \nabla \Phi_e \right)^2 \right) = 0

  \Lambda_h + \frac{b_p}{2} \left( \nabla \cdot \nabla \Phi_h + \frac{1}{2} \left( \nabla \Phi_h \right)^2 \right) = 0

Considering the discretized equation along the edge between nodes :math:`i` and :math:`j`:

.. math::

 \Lambda_e \cdot \textrm{NV}_{i} + \sum_j \frac{b_{n_{i,j}}}{2}\left( \textrm{SA}_{i,j} \cdot \nabla_{i,j} \Phi_{e_{i,j}} - \frac{1}{2} \textrm{EV}_{i,j} \left( \nabla_{i,j} \Phi_e \right)^2 \right) - \textrm{INT}_{i,k} \frac{b_{n_{ox}}}{x_n} = 0

  \Lambda_h \cdot \textrm{NV}_{i} + \sum_j \frac{b_{p_{i,j}}}{2}\left( \textrm{SA}_{i,j} \cdot \nabla_{i,j} \Phi_{h_{i,j}} - \frac{1}{2} \textrm{EV}_{i,j} \left( \nabla_{i,j} \Phi_h \right)^2 \right) - \textrm{INT}_{i,k} \frac{b_{p_{ox}}}{x_p} = 0

The gradient is then:

.. math::

  \nabla_{i,j} \Phi_x = \frac{\Phi_{x_j} - \Phi_{x_i}}{L_{i_j}}

The symbols have the following meaning:

========================== =========================================================================================
:math:`\textrm{NV}_{i}`    The total volume for node :math:`i` in the semiconductor
:math:`\textrm{L}_{i,j}`   The distance between nodes :math:`i` and :math:`j`
:math:`\textrm{SA}_{i,j}`  The surface area of the perpendicular bisector between nodes :math:`i` and :math:`j`
:math:`\textrm{EV}_{i,j}`  The volume for the node attributed to the edge between nodes :math:`i` and :math:`j`
:math:`\textrm{INT}_{i,k}` The surface area of the interface connecting node :math:`i` and oxide interface :math:`k`
========================== =========================================================================================


*Note that the sign on the* :math:`\textrm{EV}` *term depends on how the edge volume assembly is performed.*

Boundary Conditions
~~~~~~~~~~~~~~~~~~~

Semiconductor/Insulator interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wettstein :cite:`WettsteinVLSI2002` solves the equations in both the insulator in semiconductor materials.  For now, we consider the approach of other authors and assume that the carriers diminish quickly in the insulator :cite:`GarciaAsenov2011`.  Solving the equations in the insulator would be important for resonant tunneling between adjacent semiconductor regions :cite:`Hohr:sispad:2002`.

The calculations in the oxide are :cite:`jin2004`:

.. math::

  b_{n_{ox}} = \frac{\gamma_{n_{ox}} \hbar^2}{m_{ox}}

  x_n = \frac{\hbar}{\sqrt{2 m_{ox} \Phi_B}}

Ohmic Contacts
^^^^^^^^^^^^^^
At ohmic contacts the following boundary conditions are required to meet the equilibrium boundary condition assumption:

.. math::
  :nowrap:

  \begin{eqnarray}
  \Lambda_e =& 0\\
  \Lambda_h =& 0
  \end{eqnarray}

 
Units
~~~~~

================================================================ ================
:math:`b_n`, :math:`b_p`, :math:`b_{n_{ox}}`, :math:`b_{p_{ox}}` eV cm :math:`^2`
:math:`x_{n}`, :math:`x_{p}`                                     cm
:math:`\Lambda_e`, :math:`\Lambda_h`                             eV
================================================================ ================

.. Calculation of :math:`\Phi`
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculation
~~~~~~~~~~~

The values of :math:`\Phi_e` and :math:`\Phi_h` are from the calculation of the electron and hole density from their respective Fermi levels.

.. math::
  :nowrap:

  \begin{eqnarray}
  \Phi_e =& \frac{k T \log N_C + E_{F_n} - E_{C} - \Lambda_e}{k T}\\
  \Phi_h =& \frac{k T \log N_V - E_{F_p} + E_{V} - \Lambda_h}{k T}
  \end{eqnarray}

Notes
~~~~~

Sign Conventions
^^^^^^^^^^^^^^^^

The convention chosen in this description is the :math:`\Lambda_e` and :math:`\Lambda_h` act to reduce the electron and hole concentration.

.. math::
  :nowrap:

  \begin{eqnarray}
  n \propto \exp \left( -\Lambda_e \right)\\
  p \propto \exp \left( -\Lambda_h \right)
  \end{eqnarray}

Driving Force
^^^^^^^^^^^^^

The calculated values of :math:`\Lambda_e` and :math:`\Lambda_h` modify the driving force for current, as in other quantum correction models.

Recombination
^^^^^^^^^^^^^

In :cite:`Wettstein:sispad:2002`, the authors point out that :math:`n_i` for recombination must be scaled, to prevent large recombination near the interface.  This is since:

.. math::

   R \propto n p - n_i^2

Therefore:

.. math::

   n_i^2 \propto \exp \left( \frac{-\Lambda_e - \Lambda_h}{k T} \right)

Preventing Floating Point Exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In prototyping the DG equations, 2 points of numerical overflow where discovered.  When calculating the edge volume contribution, a heuristic like:

.. math::

   \left(\nabla_{i,j} \Phi_x\right)^2 = \left(b_x 10^8\right) \left(10^{-4}\left(\frac{\Phi_{x_j} - \Phi_{x_i}}{L_{i_j}}\right)\right)^2

was used.  In addition, it is important to make sure that updates in :math:`\Lambda_e` and :math:`\Lambda_h` are not too large to cause an overflow in the calculation of :math:`n` and :math:`p`.

.. % exp in the Le
.. math::
  :nowrap:

  \begin{eqnarray}
  n \propto \textrm{limexp}\left(\Phi_e\right) \\
  p \propto \textrm{limexp}\left(\Phi_h\right)
  \end{eqnarray}

where limiting the :math:`\exp` function is necessary to prevent overflow.

Ramping Strategies
^^^^^^^^^^^^^^^^^^

Since the classical and density gradient solutions are different, it is necessary to ramp the parameters :math:`\gamma_n`, and :math:`\gamma_p` to improve convergence.  A ramping strategy should be considered where the step change in :math:`\gamma_n` and :math:`\gamma_p` may be adjusted when a simulation fails to converge.

Meshing
^^^^^^^

To ensure accurate simulation results, it may be necessary to apply mesh refinements away from the interface, where the maximum in carrier concentrations occur.

Solving One DG Equation
^^^^^^^^^^^^^^^^^^^^^^^

For a MOS device, it makes sense to only solve the DG equation for the carrier in the channel of the device.

.. \appendix

Derivation of log form of equation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The log form
^^^^^^^^^^^^

.. math::
  :nowrap:

  \begin{eqnarray}
  \frac{\nabla^2 \sqrt{n}}{\sqrt{n}} =& u \nabla \cdot \vec{v} \\
  S_n =& \sqrt{n}\\
  u   =& \frac{1}{S_n}\\
  \nabla u =& -\frac{\nabla S_n}{S_n^2}\\
  \vec{v} =& \nabla S_n\\ 
  \nabla \cdot \vec{v} =& \nabla \cdot \nabla S_n\\ 
  \nabla \cdot \left(u \vec{v}\right) =& u\nabla \cdot \vec{v} + \vec{v} \cdot \nabla u\\
  u\nabla \cdot \vec{v} =& \nabla \cdot \left(u \vec{v}\right) - \vec{v} \cdot \nabla u\\
  u \vec{v} =& \nabla \log S_n = \frac{1}{2} \nabla \log n\\
  \vec{v} \cdot \nabla u =& -\nabla S_n \cdot \frac{\nabla S_n}{S_n^2} = -\left(\nabla \log S_n\right)^2 = -\frac{1}{4}\left(\nabla \log n\right)^2\\
  \frac{\nabla^2 \sqrt{n}}{\sqrt{n}} =& \frac{1}{2} \nabla^2 \log n + \frac{1}{4} \left(\nabla \log n\right)^2
  \end{eqnarray}

Wettstein
~~~~~~~~~

Introduction
^^^^^^^^^^^^

We start with deriving the equations in :cite:`WettsteinVLSI2002`.

.. math::
  :nowrap:

  \begin{eqnarray}
  \Lambda_e = -b_n\frac{\nabla^2 \sqrt{n}}{\sqrt{n}}\\
  \Lambda_h = -b_p\frac{\nabla^2 \sqrt{p}}{\sqrt{p}}
  \end{eqnarray}

where

.. math::
  :nowrap:

  \begin{eqnarray}
  b_n = \frac{\gamma_n\hbar^2}{6 m_n}\\
  b_p = \frac{\gamma_p\hbar^2}{6 m_p}
  \end{eqnarray}

The effect is such that:

.. math::
  :nowrap:

  \begin{eqnarray}
  n = N_{C} \exp\left(\frac{E_F - E_C - \Lambda_e }{k T}\right)\\
  p = N_{V} \exp\left(\frac{E_V - E_F - \Lambda_h }{k T}\right)
  \end{eqnarray}

and the intrinsic carrier density is now:

.. math::

  n_i^2 \propto \exp\left(\frac{-\Lambda_e - \Lambda_h}{k T} \right)

This is especially important for recombination.

For convenience we define:

.. math::
  :nowrap:

  \begin{eqnarray}
  n = \exp\left(\frac{\Phi_e }{k T}\right)\\
  p = \exp\left(\frac{\Phi_h }{k T}\right)
  \end{eqnarray}

where

.. math::
  :nowrap:

  \begin{eqnarray}
  \Phi_e = E_F - E_C - \Phi_C - \Lambda_e \\
  \Phi_h = E_V - E_F + \Phi_V - \Lambda_h \\
  \end{eqnarray}

where

.. math::
  :nowrap:

  \begin{eqnarray}
  \Phi_C =& -k T \log(N_C)\\
  \Phi_V =& k T \log(N_V)
  \end{eqnarray}
 
For current conduction, the effect is that:

.. math::
  :nowrap:

  \begin{eqnarray}
  J_n =& n \mu \nabla \left(\Phi_e\right)  + q D_n \nabla n \\
  J_p =& p \mu \nabla \left(\Phi_h\right)  - q D_p \nabla p
  \end{eqnarray}

where

.. math::
  :nowrap:

  \begin{eqnarray}
  \Phi_C =& -k T \log(N_C)\\
  \Phi_V =& k T \log(N_V)
  \end{eqnarray}

Method 1
^^^^^^^^


In the derivation which follows, they exploit the following relation:

.. math::
  \frac{\nabla^2 \sqrt{n}}{\sqrt{n}} = \frac{1}{2} \left\{\nabla^2 \log n + \frac{1}{2} \left(\nabla \log n\right)^2\right\}

For a volume integration:

.. math::
  :nowrap:

  \begin{eqnarray}
  %\int \Lambda_e \partial v = -\frac{b_n}{2} \int \left\{\nabla^2 \log n + \frac{1}{2} \left(\nabla \log n\right)^2\right\} \partial v\\
  %\int \Lambda_e \partial v = -\frac{b_n}{2} \int  \left\{\nabla \cdot \nabla \log n + \frac{1}{2} \left(\nabla \log n\right)^2\right\} \partial v \\
  \int \Lambda_e \partial v = - \frac{b_n}{2} \left\{ \int \nabla \log n \cdot \partial s + \frac{1}{2} \int \left(\nabla \log n\right)^2 \partial v \right\}\\
  \int \Lambda_h \partial v = - \frac{b_p}{2} \left\{ \int \nabla \log p \cdot \partial s + \frac{1}{2} \int \left(\nabla \log p\right)^2 \partial v \right\}
  \end{eqnarray}

When assembled onto node :math:`i` with respect to nodes :math:`j`.

.. math::
  :nowrap:

  \begin{eqnarray}
  \Lambda_{e,i} \Omega_i = \sum_j \frac{b_n \sigma_{i,j}}{2 l_{i,j}} \left\{ \left(\frac{\Phi_{e,j} -\Phi_{e,i}}{k T} \right) - \frac{1}{4} \left(\frac{\Phi_{e,j} -\Phi_{e,i}}{k T} \right)^2 \right\}\\
  \Lambda_{h,i} \Omega_i = \sum_j \frac{b_p \sigma_{i,j}}{2 l_{i,j}} \left\{ \left(\frac{\Phi_{h,j} -\Phi_{h,i}}{k T} \right) - \frac{1}{4} \left(\frac{\Phi_{h,j} -\Phi_{h,i}}{k T} \right)^2 \right\}
  \end{eqnarray}

Method 2
^^^^^^^^

Following :cite:`WettsteinDissertation` they discretize:

.. math::
  :nowrap:

  \begin{eqnarray}
  %\int \Lambda_e \partial v = -b_n \int \frac{\nabla^2 \sqrt{n}}{\sqrt{n}} \partial v\\
  %\int \Lambda_e \partial v = -b_n \int \frac{\nabla \cdot \nabla \sqrt{n}}{\sqrt{n}} \partial v\\
  \int \Lambda_e \partial v = -b_n \int \frac{\nabla \sqrt{n}}{\sqrt{n}} \cdot \partial s\\
  \int \Lambda_h \partial v = -b_p \int \frac{\nabla \sqrt{p}}{\sqrt{p}} \cdot \partial s
  \end{eqnarray}

When assembled onto node :math:`i` with respect to nodes :math:`j`.

.. math::
  :nowrap:

  \begin{eqnarray}
  \Lambda_i \Omega_i = \sum_j \frac{b_n \sigma_{i,j}}{l_{i,j}} \left(\frac{\sqrt{n_i} - \sqrt{n_j}}{\sqrt{n_i}} \right)\\
  \Lambda_i \Omega_i = \sum_j \frac{b_n \sigma_{i,j}}{l_{i,j}} \left(1 - \frac{\sqrt{n_j}}{\sqrt{n_i}} \right)
  \end{eqnarray}

Which then leads to:

.. math::
  :nowrap:

  \begin{eqnarray}
  \Lambda_{e,i} \Omega_i = \sum_j \frac{b_n \sigma_{i,j}}{l_{i,j}} \left\{ 1 - \exp\left(\frac{\Phi_{e,i}}{2 k T} - \frac{\Phi_{e,j}}{2 k T} \right) \right\}\\
  \Lambda_{h,i} \Omega_i = \sum_j \frac{b_n \sigma_{i,j}}{l_{i,j}} \left\{ 1 - \exp\left(\frac{\Phi_{h,i}}{2 k T} - \frac{\Phi_{h,j}}{2 k T} \right) \right\}
  \end{eqnarray}


.. 
.. 
.. %\subsection{Result}
.. %
.. %
.. %Looking at both methods, one seems to be the taylor approximation of the other.
.. %\section{Introduction}
.. %\begin{eqnarray*}
.. %\nabla^{2} \varphi =& -\frac{q}{\epsilon} \left( p - n + N_{D} - N_{A} \right)\\
.. %\frac{\partial n}{\partial t} =&  \frac{1}{q} \nabla \cdot \vec{J_{n}} + G_{n} - R_{n}\\
.. %\frac{\partial p}{\partial t} =&  -\frac{1}{q} \nabla \cdot \vec{J_{p}} + G_{p} - R_{p}\\
.. %J_n =& q n \mu E + q D \nabla n\\
.. %J_p =& q p \mu E - q D \nabla p\\
.. %\end{eqnarray*}
.. %In this :math:`E` can be:
.. %math::
.. %E = -\nabla\varphi
.. %math::
.. %\varphi = \frac{1}{q} \left(E_F - E_c\right) - \varphi_A
.. %math::
.. %\frac{\nabla^2 \sqrt{n}}{\sqrt{n}} = \frac{1}{2} \left(\nabla^2 \log n + \frac{1}{2} \left(\nabla \log n\right)^2\right)
.. %
.. %% additional eq
.. %\begin{eqnarray}
.. %\end{eqnarray}
.. %\subsection{:math:`\sqrt{n}` approach}
.. %\subsection{Sharfetter-Gummel}
.. %\subsection{Quasi-Fermi Quantum Correction Approaches}
.. %\subsubsection{Introduction}
.. %There are 2 approaches that we will focus on in this document.
.. %\subsubsection{Garcia-Loureiro Finite-Element Approach}
.. %\subsubsection{Wettstein Drift-Diffusion Simulator Approach}
.. %\begin{tabular}{l|l}
.. %sqrt n & FVM \\
.. %SG Approach & FVM \\
.. %Garcia (GSS) & FEM (3D), FD (1D)\\
.. %Wettstein (ISE) & FVM \\
.. %\end{tabular}
.. %
.. %\section{Interfaces}
.. %\section{Oxides}
.. %\section{Boundary Conditions}
.. %\section{Bulk}
.. %\section{Tunneling Effects}
.. %\section{Hydro}
.. 
.. \addcontentsline{toc}{section}{Bibliography}
.. \bibliographystyle{ieeetr}
.. \bibliography{myabbrev,dg}
.. \end{document}
.. 
