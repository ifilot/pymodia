[![CI](https://github.com/ifilot/pymodia/actions/workflows/ci.yml/badge.svg)](https://github.com/ifilot/pymodia/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pymodia?style=flat-square)](https://pypi.org/project/pymodia/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# PyMODIA

## Purpose

PyMoDia is a python package designed for making SVG images of 
[molecular orbital diagrams](https://en.wikipedia.org/wiki/Molecular_orbital_diagram) 
based on atomic orbital energies, molecular orbital energies and orbital
coefficients. These energies and coefficients can either be obtained by using
electronic structure calculation or be assumed to giving rise to qualitative
diagrams.

This package makes use of the [drawsvg](https://github.com/cduck/drawsvg) package 
to produce the SVG images. SVG images are vector based meaning that they are 
great for digital purposes.

## Documentation

PyMoDia comes with detailed documentation and examples, which can be found
at https://ifilot.github.io/pymodia/.

## Installation

PyMODIA is best used in its own environment which can be created and activated
via

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install PyMoDia via

```bash
pip install -e .
```

The `-e` directive ensures that if you make changes to the PyMODIA sources,
they will be automatically propagated to the environment.

Besides, `numpy` and `drawsvg` as the core dependencies, we recommend also
installing `pyqint` and `pydft` to run the majority of the examples.

```bash
pip install pyqint pydft
```

## Gallery

![MO diagram for canonical MO of CO](img/mo_co_canonical.png)![MO diagram for localized MO of CO](img/mo_co_localized.png)

![MO diagram for canonical MO of CH4](img/mo_ch4_canonical.png)![MO diagram for localized MO of CH4](img/mo_ch4_localized.png)

![MO diagram for canonical MO of ethylene](img/mo_ethylene_canonical.png)![MO diagram for localized MO of ethylene](img/mo_ethylene_localized.png)