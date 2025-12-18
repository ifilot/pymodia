.. _installation:
.. index:: Installation

Installation
============

Package availability
--------------------

:program:`PyMoDia` is distributed via the Python Package Index (PyPI) and can be
installed using the standard Python package manager ``pip``.

The recommended way to use :program:`PyMoDia` is within a **dedicated Python
environment**, which avoids dependency conflicts and ensures reproducible
results.

Creating a separate Python environment
--------------------------------------

It is strongly recommended to install :program:`PyMoDia` in a clean virtual
environment rather than into a system-wide Python installation.

Using ``venv`` (Python ≥ 3.8)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new virtual environment:

.. code-block:: bash

   python -m venv pymodia-env

Activate the environment:

- On Linux or macOS:

  .. code-block:: bash

     source pymodia-env/bin/activate

- On Windows:

  .. code-block:: powershell

     pymodia-env\Scripts\activate

Once activated, all installed packages will be isolated within this environment.

Installing PyMoDia
------------------

With the environment activated, install :program:`PyMoDia` from PyPI:

.. code-block:: bash

   pip install pymodia

This will install :program:`PyMoDia` along with its required visualization
dependencies.

Electronic structure backends
------------------------------

:program:`PyMoDia` itself is a **visualization package**.
It does *not* perform electronic structure calculations.

To construct molecular orbital diagrams directly from *ab initio* electronic
structure data, an external quantum-chemical backend is required.

Currently supported backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `PyQInt <https://github.com/ifilot/pyqint>`_
- `PyDFT <https://github.com/ifilot/pydft>`_ (experimental)

These packages provide Hartree-Fock or density-functional-theory calculations
whose results can be passed directly to :program:`PyMoDia`.

Important limitation
~~~~~~~~~~~~~~~~~~~~

Direct construction of molecular orbital diagrams from electronic structure
calculations is intended for use with **minimal basis sets** only.
Minimal basis sets preserve a clear correspondence between atomic orbitals
(AOs) and molecular orbitals (MOs), which is essential for producing meaningful
MO diagrams with explicit AO-MO connections.

For larger or highly flexible basis sets, this correspondence becomes ambiguous,
and :program:`PyMoDia` is therefore not designed to visualize such results.

Summary
-------

- :program:`PyMoDia` is installed via PyPI using ``pip``.
- A separate virtual environment is strongly recommended.
- :program:`PyMoDia` does **not** perform electronic structure calculations.
- To build MO diagrams from computed wavefunctions, a backend such as
  `PyQInt <https://github.com/ifilot/pyqint>`_ is required.
- Direct AO-MO diagram construction is intended for **minimal basis sets** only.