# -*- coding: utf-8 -*-

"""
strain_step
A SEAMM plug-in for straining periodic systems
"""

import copy

import seamm

# Bring up the classes so that they appear to be directly in
# the strain_step package.

from .strain import Strain  # noqa: F401
from .strain_parameters import StrainParameters  # noqa: F401
from .strain_step import StrainStep  # noqa: F401
from .tk_strain import TkStrain  # noqa: F401

from .metadata import metadata  # noqa: F401

# Handle versioneer
from ._version import get_versions

# How the strained structure is handled: SEAMM's standard structure handling,
# less the choices that make no sense here -- a strain makes one structure, and
# discarding it would leave nothing -- defaulting, as before, to a new
# configuration named after the strain.
structure_handling_parameters = copy.deepcopy(
    seamm.standard_parameters.structure_handling_parameters
)
del structure_handling_parameters["subsequent structure handling"]
_handling = structure_handling_parameters["structure handling"]
_handling["default"] = "Create a new configuration"
_handling["enumeration"] = tuple(
    e for e in _handling["enumeration"] if e != "Discard the structure"
)
_handling["description"] = "Strained structure:"
structure_handling_parameters["system name"]["default"] = "keep current name"
_names = structure_handling_parameters["configuration name"]
#: Names the configuration after the strains, e.g. 'strained by (0.01, 0, 0, 0, 0, 0)'
STRAIN_NAME = "strained by <strain vector>"
_names["default"] = STRAIN_NAME
_names["enumeration"] = (STRAIN_NAME, *_names["enumeration"])
del _handling, _names

__author__ = "Paul Saxe"
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
