# -*- coding: utf-8 -*-

"""
strain_step
A SEAMM plug-in for straining periodic systems
"""

# Bring up the classes so that they appear to be directly in
# the strain_step package.

from .strain import Strain  # noqa: F401
from .strain_parameters import StrainParameters  # noqa: F401
from .strain_step import StrainStep  # noqa: F401
from .tk_strain import TkStrain  # noqa: F401

from .metadata import metadata  # noqa: F401

# Handle versioneer
from ._version import get_versions

# Parameters used for handling the structure if it is changed.
structure_handling_parameters = {
    "structure handling": {
        "default": "be put in a new configuration",
        "kind": "enum",
        "default_units": "",
        "enumeration": (
            "overwrite the current configuration",
            "be put in a new configuration",
        ),
        "format_string": "s",
        "description": "Strained structure will",
        "help_text": (
            "Whether to overwrite the current configuration, or create a new "
            "configuration or system and configuration for the new structure"
        ),
    },
    "configuration name": {
        "default": "strained by <strain vector>",
        "kind": "string",
        "default_units": "",
        "enumeration": (
            "strained by <strain vector>",
            "keep current name",
            "use SMILES string",
            "use Canonical SMILES string",
            "use configuration number",
        ),
        "format_string": "s",
        "description": "Configuration name:",
        "help_text": "The name for the new configuration",
    },
}

__author__ = "Paul Saxe"
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
