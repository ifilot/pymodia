.. _usage:
.. index:: usage

Using PyMoDia
=============

Overview
--------

:program:`PyMoDia` provides a Python-based interface for constructing and
rendering molecular orbital (MO) diagrams.
Rather than offering a graphical user interface, interaction with PyMoDia
is performed entirely through Python objects that represent molecular data,
fragments, and visualization settings.

The typical workflow consists of:
  - Preparing molecular orbital data.
  - Constructing fragment definitions.
  - Combining this information into a diagram data container.
  - Customizing visualization options.
  - Rendering and exporting the diagram.

Core concepts
-------------

Molecule and fragments
~~~~~~~~~~~~~~~~~~~~~~

At the heart of PyMoDia is the distinction between the **molecule** and its
**fragments**.

- A :class:`MoDiaMolecule` object stores molecular orbital energies, orbital
  coefficients, and the total number of electrons.
- One or more :class:`MoDiaFragment` objects describe atomic or molecular
  fragments, including their local orbital energies and electron counts.

This separation allows PyMoDia to visualize how fragment orbitals combine to
form molecular orbitals.

Data container
~~~~~~~~~~~~~~

The :class:`MoDiaData` class acts as a container that combines a molecule and
its fragments into a single object.
It performs bookkeeping tasks such as:

 - Storing orbital energies used for plotting.
 - Managing fragment–molecule orbital mappings.
 - Providing a consistent interface to the diagram renderer.

Diagram construction
--------------------

The actual MO diagram is created using the :class:`MoDia` class.
This class takes a :class:`MoDiaData` instance and optional visualization
settings, and is responsible for assembling and rendering the diagram.

A minimal example looks like:

.. code-block:: python

   data = MoDiaData(molecule, fragment1, fragment2)
   diagram = MoDia(data)
   diagram.export_svg("mo_diagram.svg")

Visualization settings
----------------------

The appearance of the diagram is controlled through a
:class:`MoDiaSettings` object.
This object groups all visual parameters, such as:

  - Orbital and arrow colors
  - Energy rounding
  - Cutoffs for displaying orbital coefficients
  - Label formatting

Settings can either be passed explicitly:

.. code-block:: python

   settings = MoDiaSettings()
   settings.orbc_color = "#555555"
   diagram = MoDia(data, settings=settings)

or overridden directly when constructing the diagram:

.. code-block:: python

   diagram = MoDia(data, orbc_color="#555555")

Exporting diagrams
------------------

Currently, PyMoDia exports diagrams as scalable vector graphics (SVG) files.
SVG output is resolution-independent and well suited for:

  - Lecture slides
  - Printed material
  - Web-based teaching resources

Diagrams are exported using:

.. code-block:: python

   diagram.export_svg("output.svg")

Relationship to electronic structure codes
-------------------------------------------

PyMoDia itself does not perform electronic structure calculations.
Instead, it can be coupled to external quantum-chemical Python packages,
most notably `PyQInt <https://github.com/ifilot/pyqint>`_, to construct MO
diagrams directly from computed wavefunctions.

When using electronic structure backends, PyMoDia is intended for use with
minimal basis sets, where a clear correspondence between atomic and molecular
orbitals can be established.