

Scharfetter-Gummel
------------------

Bernoulli Function
~~~~~~~~~~~~~~~~~~

This derivation is partly based on :cite:`PintoDissertation`.

Starting with

.. math::

  J = \alpha n + \beta \nabla{n}

where :math:`\beta` is a function of :math:`x`

.. math::

  \int_{x_0}^{x_1}{\frac{\partial x}{\beta}} = \int_{n_0}^{n_1}{\frac{\partial n}{J - \alpha n}}

For the left side, we assume a linear function:

.. math::

  \int_{x_0}^{x_1}{\frac{\partial x}{\beta_0 + \frac{\beta_1}{\beta_0} \frac{\left(x - x_0 \right)}{\left(x_1 - x_0 \right)} }}

where

.. math::

  \beta_0 = \beta \left( x_0 \right)

using :eq:`hf1`

.. math::

  \int_{x_0}^{x_1}{\frac{\partial x}{\beta}} &= \frac{x_1 - x_0}{\beta_1 - \beta_0} \log \frac{\beta_1}{\beta_0}

.. math:: :label: hf2

  \overline{\beta} &= \frac{\beta_1 - \beta_0}{\log \frac{\beta_1}{\beta_0}}

.. math::

  L &= {x_1 - x_0}

  \frac{L}{\overline{\beta}} &= \int_{n_0}^{n_1}{\frac{\partial n}{J - \alpha n}}


using :eq:`hf1`

.. math::

  \frac{L}{\overline{\beta}} &= \frac{-1}{\alpha}\log \frac{J - \alpha n_1}{J - \alpha n_0}

Then solving for :math:`J`

.. math::

  \frac{-\alpha L}{\overline{\beta}} &= \log \frac{J - \alpha n_1}{J - \alpha n_0}

  \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) &= \frac{J - \alpha n_1}{J - \alpha n_0}

  \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) \left({J - \alpha n_0} \right) &= {J - \alpha n_1}

  J \left( \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) - 1 \right) &= \exp \left(-\frac{\alpha L}{\overline{\beta}}\right) {\alpha n_0} - \alpha n_1

We look for a form compatible with the Bernoulli function:

.. math::

  B\left( x \right) &= \frac{x}{\exp \left(x\right) - 1}

.. math::

  J  &= \frac{\overline{\beta}}{L}\frac{\exp \left(\frac{-\alpha L}{\overline{\beta}}\right) {\frac{\alpha L}{\overline{\beta}} n_0} - {\frac{\alpha L}{\overline{\beta}} n_1}}{\left( \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) - 1 \right)}

  J  &= \frac{\overline{\beta}}{L} \left(
        \frac{\exp \left(\frac{-\alpha L}{\overline{\beta}}\right) {\frac{\alpha L}{\overline{\beta}} n_0}}{\left( \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) - 1 \right)}
        -\frac{{\frac{\alpha L}{\overline{\beta}} n_1}}{\left( \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) - 1 \right)}
        \right)

  J  &= \frac{\overline{\beta}}{L} \left(
         \frac{{\frac{\alpha L}{\overline{\beta}} n_0}}{\left( 1 - \exp \left(\frac{\alpha L}{\overline{\beta}}\right) \right)}
        -\frac{{\frac{\alpha L}{\overline{\beta}} n_1}}{\left( \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) - 1 \right)}
        \right)

  J  &= \frac{\overline{\beta}}{L} \left(
         \frac{{\frac{-\alpha L}{\overline{\beta}} n_1}}{\left( \exp \left(\frac{-\alpha L}{\overline{\beta}}\right) - 1 \right)}
        -\frac{{\frac{\alpha L}{\overline{\beta}} n_0}}{\left( \exp \left(\frac{\alpha L}{\overline{\beta}}\right) - 1 \right)}
        \right)


Associated this to the case of electrons

.. math:: :label: hfjn

  J_n  &= \frac{\overline{\beta}}{L} \left( B \left({\frac{-\alpha_n L}{\overline{\beta}} }\right) n_1  - B \left({\frac{\alpha_n L}{\overline{\beta}} }\right) n_0 \right)

For the case of holes

.. math::

  J_p &= \alpha_p p - \beta \nabla{p}

and using the same definition for :math:`\overline{\beta}` in :eq:`hf2`.

.. math::

  J_p  &= \frac{-\overline{\beta}}{L} \left( B \left({\frac{-\alpha_p L}{-\overline{\beta}} }\right) p_1  - B \left({\frac{\alpha_p L}{-\overline{\beta}} }\right) p_0 \right)

.. math:: :label: hfjp

  J_p  &= \frac{-\overline{\beta}}{L} \left( B \left({\frac{\alpha_p L}{\overline{\beta}} }\right) p_1  - B \left({\frac{-\alpha_p L}{\overline{\beta}} }\right) p_0 \right)


.. put test here

Testing Limits
~~~~~~~~~~~~~~

Using L'Hopital's Rule.

.. math::

  B\left(x\right) \Bigr|_{x \to 0} = \frac{1}{\exp\left(0\right)} = 1

and as expected for diffusion

.. math::

  J_n \Bigr|_{\alpha \to 0}  &= \frac{\overline{\beta}}{L} \left(  n_1  -  n_0 \right)

  J_p \Bigr|_{\alpha \to 0}  &= -\frac{\overline{\beta}}{L} \left(  p_1  -  p_0 \right)


For drift:

.. math::

  B\left(\frac{\alpha L}{\overline{\beta}}\right) \Bigr|_{\alpha \to \infty} &= 0

  B\left(\frac{-\alpha L}{\overline{\beta}}\right) \Bigr|_{\alpha \to \infty} &= \frac{\alpha L}{\overline{\beta}}

  B\left(\frac{\alpha L}{\overline{\beta}}\right) \Bigr|_{\alpha \to -\infty} &= \frac{-\alpha L}{\overline{\beta}}

  B\left(\frac{-\alpha L}{\overline{\beta}}\right) \Bigr|_{\alpha \to -\infty} &= 0

.. math::

  J_n \Bigr|_{\alpha \to \infty}  &= \alpha n_1

  J_n \Bigr|_{\alpha \to -\infty}  &= \alpha n_0

or

.. math::

  J_p \Bigr|_{\alpha \to \infty}  &= \alpha p_0

  J_p \Bigr|_{\alpha \to -\infty}  &= \alpha p_1

Evaluate Bernoulli
~~~~~~~~~~~~~~~~~~

This requires an expansion near :math:`0` and use of :eq:`hf4`.

.. math::

  \begin{cases}
    x < 0 & B\left(-x\right)    = B\left(x\right) + x\\
    x < \text{lim1} & B\left(x\right) = \left({\sum_{n=1}^{N} \frac{1}{\left(n+1\right)!}x^{n})}\right)^{-1}\\
    x < \text{lim2} & B\left(x\right) = \frac{x}{\exp\left(x\right) - 1}\\
    \text{else} & B\left(x\right)      = x \exp\left(-x\right)
  \end{cases}

where lim1, lim2, and :math:`N` are set appropriate for continuity and accuracy.



Helpful function
~~~~~~~~~~~~~~~~

To perform the integrals in the derivations of :eq:`hfjn`

.. math::

  \int_{x_0}^{x_1} \frac{\partial x}{a + b x}

  y = a + b x

  \partial y = b \partial x

  \frac{1}{b} \int_{y_0}^{y_1} \frac{\partial y}{y}

  \frac{1}{b} \log y \Bigr|_{y_0}^{y_1}

  \frac{1}{b} \log \frac{y_1}{y_0}

.. math:: :label: hf1

  \int_{x_0}^{x_1} \frac{\partial x}{a + b x} &= \frac{1}{b} \log \frac{a + b x_1}{a + b x_0}


To reduce the number of computations for :eq:`hfjn` and :eq:`hfjp`:

.. math::

  B\left(x\right) &= \frac{x}{\exp\left(x\right) - 1}

  B\left(x\right) \exp\left(x\right) - B\left(x\right)&= x

  B\left(x\right) &= B\left(x\right) \exp\left(x\right) - x

  B\left(x\right) &= \frac{x}{\exp\left(x\right) - 1} \exp\left(x\right) - x

  B\left(x\right) &=  \frac{x \exp\left(x\right)}{\exp\left(x\right) - 1} - x

  B\left(x\right) &=  \frac{x}{1 - \exp\left(-x\right)} - x

  B\left(x\right) &=  \frac{-x}{\exp\left(-x\right) - 1} - x

  B\left(x\right) &= B\left(-x\right) - x

.. math:: :label: hf4

  B\left(-x\right) &= B\left(x\right) + x


.. expansions here

.. limits here


Driving Force
~~~~~~~~~~~~~

For Electrons:
^^^^^^^^^^^^^^

.. math::

  J_n &= J_{drift} + J_{diffusion}

  J_{diffusion} &= q \nabla \left(D_n n\right)

At equilibrium:

.. math::

  J_n = 0 &= J_{drift} + q D_n \nabla n + q n \nabla D_n

  J_{drift} &= - q D_n \nabla n - q n \nabla  D_n

Assuming no temperature gradient:

.. math::

  J_{drift} &= - q D_n \nabla n

  n &= N_c \gamma_n \exp \left(\frac{E_F - E_c}{k T}\right)

  \nabla n &= n \left( \frac{\nabla N_c}{N_c} + \frac{\nabla \gamma_n}{\gamma_n}  - \nabla\left(\frac{E_c}{k T}\right)\right)

  \nabla n &= n \left( {\nabla \log\left(N_c\right)} + {\nabla \log\left(\gamma_n\right)}  - \nabla\left(\frac{E_c}{k T}\right)\right)

  J_{drift} &= - q D_n  n \left( {\nabla \log\left(N_c\right)} + {\nabla \log\left(\gamma_n\right)}  - \nabla\left(\frac{E_c}{k T}\right)\right)

  J_{drift} &= q D_n  n \left( \nabla\left(\frac{E_c}{k T}\right) - {\nabla \log\left(N_c \gamma_n \right)}\right)


Then in general:

.. math::

  J_n &= q D_n  n \left( \nabla\left(\frac{E_c}{k T}\right) - {\nabla \log\left(N_c \gamma_n \right)}\right) + q D_n \nabla n + q n \nabla D_n

  J_n &= q D_n  n \left( \nabla\left(\frac{E_c}{k T}\right) - {\nabla \log\left(N_c \gamma_n \right)} + \frac{\nabla D_n}{D_n}\right) + q D_n \nabla n

  D_n &= \frac{k T \mu_n}{q}

  J_n &= {k T \mu_n}  n \left( \nabla\left(\frac{E_c}{k T}\right) - {\nabla \log\left(N_c \gamma_n \right)} + \frac{\nabla T}{T}\right) + {k T \mu_n} \nabla n

  \frac{J_n}{k \mu_n} &= {T} \left( \nabla\left(\frac{E_c}{k T}\right) - {\nabla \log\left(N_c \gamma_n \right)} + \frac{\nabla T}{T}\right) n + {T} \nabla n

Using:

.. math::

  \alpha_n &= {T} \left( \nabla\left(\frac{E_c}{k T}\right) - {\nabla \log\left(N_c \gamma_n \right)} + \frac{\nabla T}{T}\right)

and assuming that the derivatives from :math:`x_0` to :math:`x_1` are constant:

.. math::

  \alpha_n &= \frac{\alpha_{n_1} - \alpha_{n_0}}{L}

where

.. math::

  \alpha_{n_i} &= {\overline{T}} \left( \frac{E_{c_{i}}}{k T_i} - {\log\left(N_{c_{i}} \gamma_{n_{i}} \right)} + \frac{T_i}{\overline{T}}\right)

.. math:: :label: hftave

  \overline{T} &= \frac{T_1 + T_0}{2}


.. math::

  \beta &= T

using :eq:`hf2`

.. math::

  \overline{\beta} &= \frac{T_1 - T_0}{\log \frac{T_1}{T_0}}

can be shown to be

.. math:: :label: hfbeta

  \overline{\beta} &= \frac{T_0}{B\left(\log\frac{T_1}{T_0}\right)}


For Holes:
^^^^^^^^^^

.. math::

  J_{drift} &= q D_p \nabla p

  p &= N_v \gamma_p \exp \left(\frac{E_v - E_F}{k T}\right)

  \nabla p &= p \left( \frac{\nabla N_v}{N_v} + \frac{\nabla \gamma_p}{\gamma_p}  + \nabla\left(\frac{E_v}{k T}\right)\right)

  \nabla p &= p \left( {\nabla \log\left(N_v\right)} + {\nabla \log\left(\gamma_p\right)}  + \nabla\left(\frac{E_v}{k T}\right)\right)

  J_{drift} &= q D_p  p \left( {\nabla \log\left(N_v\right)} + {\nabla \log\left(\gamma_p\right)}  + \nabla\left(\frac{E_v}{k T}\right)\right)

  J_{drift} &= q D_p  p \left( \nabla\left(\frac{E_v}{k T}\right) + {\nabla \log\left(N_v \gamma_p \right)}\right)


Then in general:

.. math::

  J_p &= q D_p  p \left( \nabla\left(\frac{E_v}{k T}\right) + {\nabla \log\left(N_v \gamma_p \right)}\right) - q D_p \nabla p - q p \nabla D_p

  J_p &= q D_p  p \left( \nabla\left(\frac{E_v}{k T}\right) + {\nabla \log\left(N_v \gamma_p \right)} - \frac{\nabla D_p}{D_p}\right) - q D_p \nabla p

  D_p &= \frac{k T \mu_p}{q}

  J_p &= {k T \mu_p}  p \left( \nabla\left(\frac{E_v}{k T}\right) + {\nabla \log\left(N_v \gamma_p \right)} - \frac{\nabla T}{T}\right) - {k T \mu_p} \nabla p

  \frac{J_p}{k \mu_p} &= {T} \left( \nabla\left(\frac{E_v}{k T}\right) + {\nabla \log\left(N_v \gamma_p \right)} - \frac{\nabla T}{T}\right) p - {T} \nabla p


Then :eq:`hfbeta` is used to calculate :math:`\overline{\beta}` and :eq:`hftave` is used to calculate :math:`\overline{T}`.

.. math::

  \alpha_{p_i} &= {\overline{T}} \left( \frac{E_{v_{i}}}{k T_i} + {\log\left(N_{v_{i}} \gamma_{p_{i}} \right)} - \frac{T_i}{\overline{T}}\right)


Temperature:
^^^^^^^^^^^^

For the case of carrier temperatures, then :math:`T_n` and :math:`T_p` are substituted into :math:`\overline{\beta}` and :math:`T` as appropriate.

.. math:{\beta}` is carrier dependent.

