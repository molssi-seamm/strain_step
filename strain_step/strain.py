# -*- coding: utf-8 -*-

"""Non-graphical part of the Strain step in a SEAMM flowchart"""

import logging
from pathlib import Path
import pprint  # noqa: F401
import textwrap

from tabulate import tabulate

import strain_step
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: "job" and "printer". "job" send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# "printer" sends output to the file "step.out" in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("Strain")


class Strain(seamm.Node):
    """
    The non-graphical part of a Strain step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : StrainParameters
        The control parameters for Strain.

    See Also
    --------
    TkStrain,
    Strain, StrainParameters
    """

    def __init__(self, flowchart=None, title="Strain", extension=None, logger=logger):
        """A step for Strain in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug(f"Creating Strain {self}")

        super().__init__(
            flowchart=flowchart,
            title="Strain",
            extension=extension,
            module=__name__,
            logger=logger,
        )  # yapf: disable

        self.parameters = strain_step.StrainParameters()

    @property
    def version(self):
        """The semantic version of this module."""
        return strain_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return strain_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        text = "If the system is periodic it will be strained as follows:\n\n"
        text = self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

        epsilon = "\N{GREEK SMALL LETTER EPSILON}"
        table = {}
        table["Direction"] = (
            f"{epsilon}(xx) = {epsilon}\N{SUBSCRIPT ONE}",
            f"{epsilon}(yy) = {epsilon}\N{SUBSCRIPT TWO}",
            f"{epsilon}(zz) = {epsilon}\N{SUBSCRIPT THREE}",
            f"2{epsilon}(yz) = {epsilon}\N{SUBSCRIPT FOUR}",
            f"2{epsilon}(xz) = {epsilon}\N{SUBSCRIPT FIVE}",
            f"2{epsilon}(xy) = {epsilon}\N{SUBSCRIPT SIX}",
        )
        table["Strain"] = (
            P["strain_xx"],
            P["strain_yy"],
            P["strain_zz"],
            P["strain_yz"],
            P["strain_xz"],
            P["strain_xy"],
        )
        text += "                       Strains\n"
        text += textwrap.indent(
            tabulate(
                table,
                headers="keys",
                tablefmt="psql",
                colalign=("right", "decimal"),
            ),
            self.indent + 12 * " ",
        )
        text += "\n\n"
        text += __(
            seamm.standard_parameters.structure_handling_description(P),
            indent=4 * " ",
        ).__str__()

        return text

    def run(self):
        """Run a Strain step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # The current system and configuration, before any new one is made
        starting_system, starting_configuration = self.get_system_configuration(None)

        periodicity = starting_configuration.periodicity
        if periodicity != 3:
            printer.important(
                __("System is not periodic, so doing nothing.", indent=self.indent)
            )
            return next_node

        # Print what we are doing
        printer.important(__(self.description_text(P), indent=self.indent))

        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        # Before straining: with "Overwrite the current configuration" the
        # starting configuration is the one strained.
        initial_cell = starting_configuration.cell.parameters

        # The standard structure handling: overwrite, or a copy in a new
        # configuration or a new system
        system, configuration = self.get_system_configuration(P)

        strains = [
            P[key]
            for key in (
                "strain_xx",
                "strain_yy",
                "strain_zz",
                "strain_yz",
                "strain_xz",
                "strain_xy",
            )
        ]
        configuration.strain(*strains)

        names = dict(P)
        if names["configuration name"] == strain_step.STRAIN_NAME:
            vector = ", ".join(f"{s:g}" for s in strains)
            names["configuration name"] = f"strained by ({vector})"
        # "keep current name" carries the names over to a new system or
        # configuration
        if (
            system is not starting_system
            and names["system name"] == "keep current name"
        ):
            system.name = starting_system.name
        if configuration.id != starting_configuration.id and names[
            "configuration name"
        ] == ("keep current name"):
            configuration.name = starting_configuration.name
        text = seamm.standard_parameters.set_names(system, configuration, names)
        printer.important(__(text, indent=self.indent + 4 * " "))
        printer.important("")

        table = {}
        table["Parameter"] = (
            "a",
            "b",
            "c",
            "\N{GREEK SMALL LETTER ALPHA}",
            "\N{GREEK SMALL LETTER BETA}",
            "\N{GREEK SMALL LETTER GAMMA}",
        )
        table["Initial"] = initial_cell
        table["Final"] = configuration.cell.parameters

        text = ""
        text += "                     Strained Cell\n"
        text += textwrap.indent(
            tabulate(
                table,
                headers="keys",
                tablefmt="psql",
                colalign=("center", "decimal", "decimal"),
            ),
            self.indent + 7 * " ",
        )
        printer.important(text)

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        return next_node

    def analyze(self, indent="", **kwargs):
        """Do any analysis of the output from this step.

        Also print important results to the local step.out file using
        "printer".

        Parameters
        ----------
        indent: str
            An extra indentation for the output
        """
        printer.normal(
            __(
                "This is a placeholder for the results from the Strain step",
                indent=4 * " ",
                wrap=True,
                dedent=False,
            )
        )
