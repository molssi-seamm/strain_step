# -*- coding: utf-8 -*-
"""Control parameters for the Strain step in a SEAMM flowchart.
"""

import logging

import seamm
import strain_step

logger = logging.getLogger(__name__)


class StrainParameters(seamm.Parameters):
    """The control parameters for Strain.

    The developer will add a dictionary of Parameters to this class.
    The keys are parameters for the current plugin, which themselves
    might be dictionaries.

    You need to replace the "time" example below with one or more
    definitions of the control parameters for your plugin and application.

    parameters : {str: {str: str}}
        A dictionary containing the parameters for the current step.
        Each key of the dictionary is a dictionary that contains the
        the following keys: kind, default, default_units, enumeration,
        format_string, description and help text.

    parameters["kind"]: custom
        Specifies the kind of a variable. While the "kind" of a variable might
        be a numeric value, it may still have enumerated custom values
        meaningful to the user. For instance, if the parameter is
        a convergence criterion for an optimizer, custom values like "normal",
        "precise", etc, might be adequate. In addition, any
        parameter can be set to a variable of expression, indicated by having
        "$" as the first character in the field. For example, $OPTIMIZER_CONV.

    parameters["default"] : "integer" or "float" or "string" or "boolean" or
        "enum" The default value of the parameter, used to reset it.

    parameters["default_units"] : str
        The default units, used for resetting the value.

    parameters["enumeration"]: tuple
        A tuple of enumerated values.

    parameters["format_string"]: str
        A format string for "pretty" output.

    parameters["description"]: str
        A short string used as a prompt in the GUI.

    parameters["help_text"]: tuple
        A longer string to display as help for the user.

    See Also
    --------
    Strain, TkStrain, Strain
    StrainParameters, StrainStep

    Examples
    --------
    ::

        parameters = {
            "time": {
                "default": 100.0,
                "kind": "float",
                "default_units": "ps",
                "enumeration": tuple(),
                "format_string": ".1f",
                "description": "Simulation time:",
                "help_text": ("The time to simulate in the dynamics run.")
            },
        }
    """

    parameters = {
        "strain_xx": {
            "default": 0.0,
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": (
                "\N{GREEK SMALL LETTER EPSILON}(xx) = "
                "\N{GREEK SMALL LETTER EPSILON}\N{SUBSCRIPT ONE}:"
            ),
            "help_text": "Strain in the XX direction.",
        },
        "strain_yy": {
            "default": 0.0,
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": (
                "\N{GREEK SMALL LETTER EPSILON}(yy) = "
                "\N{GREEK SMALL LETTER EPSILON}\N{SUBSCRIPT TWO}:"
            ),
            "help_text": "Strain in the YY direction.",
        },
        "strain_zz": {
            "default": 0.0,
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": (
                "\N{GREEK SMALL LETTER EPSILON}(zz) = "
                "\N{GREEK SMALL LETTER EPSILON}\N{SUBSCRIPT THREE}:"
            ),
            "help_text": "Strain in the ZZ direction.",
        },
        "strain_yz": {
            "default": 0.0,
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": (
                "2\N{GREEK SMALL LETTER EPSILON}(yz) = "
                "\N{GREEK SMALL LETTER EPSILON}\N{SUBSCRIPT FOUR}:"
            ),
            "help_text": "Strain in the YZ direction.",
        },
        "strain_xz": {
            "default": 0.0,
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": (
                "2\N{GREEK SMALL LETTER EPSILON}(xz) = "
                "\N{GREEK SMALL LETTER EPSILON}\N{SUBSCRIPT FIVE}:"
            ),
            "help_text": "Strain in the XZ direction.",
        },
        "strain_xy": {
            "default": 0.0,
            "kind": "float",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": ".3f",
            "description": (
                "2\N{GREEK SMALL LETTER EPSILON}(xy) = "
                "\N{GREEK SMALL LETTER EPSILON}\N{SUBSCRIPT SIX}:"
            ),
            "help_text": "Strain in the XY direction.",
        },
    }

    def __init__(self, defaults={}, data=None):
        """
        Initialize the parameters, by default with the parameters defined above

        Parameters
        ----------
        defaults: dict
            A dictionary of parameters to initialize. The parameters
            above are used first and any given will override/add to them.
        data: dict
            A dictionary of keys and a subdictionary with value and units
            for updating the current, default values.

        Returns
        -------
        None
        """

        logger.debug("StrainParameters.__init__")

        super().__init__(
            defaults={
                **StrainParameters.parameters,
                **strain_step.structure_handling_parameters,
                **defaults,
            },
            data=data,
        )
