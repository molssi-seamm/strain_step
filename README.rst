====================
SEAMM Strain Plug-in
====================

.. image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/strain_step
   :target: https://github.com/molssi-seamm/strain_step/pulls
   :alt: GitHub pull requests

.. image:: https://github.com/molssi-seamm/strain_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/strain_step/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/strain_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/strain_step
   :alt: Code Coverage

.. image:: https://img.shields.io/lgtm/grade/python/g/molssi-seamm/strain_step.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/molssi-seamm/strain_step/context:python
   :alt: Code Quality

.. image:: https://github.com/molssi-seamm/strain_step/workflows/Documentation/badge.svg
   :target: https://molssi-seamm.github.io/strain_step/index.html
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/strain_step.svg
   :target: https://pypi.python.org/pypi/strain_step
   :alt: PyPi VERSION

A SEAMM plug-in for straining periodic systems.

* Free software: BSD-3-Clause
* Documentation: https://molssi-seamm.github.io/strain_step/index.html
* Code: https://github.com/molssi-seamm/strain_step

Features
--------

Applies an arbitrary strain to the system, using input in `Voigt notation`_. Note the
factor of two in the engineering shear strains, which is the normal convention used in
simulations. Other than that, there really isn't much to say about this plug-in! It is
simple, and it works.

.. _`Voigt notation`: https://en.wikipedia.org/wiki/Voigt_notation

Acknowledgements
----------------

This package was created with Cookiecutter_ and the
`molssi-seamm/cookiecutter-seamm-plugin`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the `National Science Foundation`_ under
award CHE-2136142.

.. _MolSSI: https://molssi.org
.. _`National Science Foundation`: https://www.nsf.gov
