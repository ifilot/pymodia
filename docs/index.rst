.. image:: _static/img/banner.svg
  :width: 600
  :alt: PyMoDia logo

=======

:program:`PyMoDia` is primarily intended for educational use.
Its main purpose is to produce clear and intuitive visualizations of molecular
orbital structures that can be used in teaching and learning environments.
Educators can perform electronic structure calculations and subsequently use
:program:`PyMoDia` to generate illustrative figures or student exercises.

In addition to qualitative, textbook-style diagrams,
:program:`PyMoDia` can be coupled to quantum-chemical Python packages to
visualize results obtained from *ab initio* electronic structure calculations.
At present, the direct construction of molecular orbital diagrams from
quantum-chemical calculations is supported exclusively through
`PyQInt <https://github.com/ifilot/pyqint>`_.
This approach is intended for use with **minimal basis sets**, where a clear
one-to-one correspondence between atomic orbitals and molecular orbitals can
be established, allowing meaningful AO-MO level connections to be visualized.

Several examples demonstrating this workflow are provided in the
:ref:`examples <examples>` section.

.. figure:: _static/img/mo_co_canonical.svg
   :align: center
   :width: 600
   :alt: simple H2 molecular orbital diagram

   Molecular orbital diagram of CO. Script used to make this image can be found in :ref:`example <examples>`

:program:`PyMoDia` has been developed at the Eindhoven University of Technology, Netherlands.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   examples
   community_guidelines

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
