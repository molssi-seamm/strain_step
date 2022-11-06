# -*- coding: utf-8 -*-

"""
strain_step
A SEAMM plug-in for straining periodic systems
"""

# Bring up the classes so that they appear to be directly in
# the strain_step package.

from .strain import Strain  # noqa: F401, E501
from .strain_parameters import StrainParameters  # noqa: F401, E501
from .strain_step import StrainStep  # noqa: F401, E501
from .tk_strain import TkStrain  # noqa: F401, E501

from .metadata import metadata  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = "Paul Saxe"
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
