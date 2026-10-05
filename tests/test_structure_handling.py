# -*- coding: utf-8 -*-

"""The strained structure's handling: SEAMM's standard choices and names.

End to end, a flowchart (a tiny cubic crystal step, then Strain) is built from a
spec and run by ``run_flowchart`` (seamm_exec.testing); the result is read from
the job's database.
"""

import sqlite3
import textwrap
from pathlib import Path

import pytest

from strain_step import STRAIN_NAME, StrainParameters

SOURCE = Path(__file__).resolve().parents[1]

CUBIC_STEP = textwrap.dedent('''
    """A step for testing: a simple cubic argon crystal, a = 3 Å."""

    import seamm


    class Cubic(seamm.Node):
        def __init__(self, flowchart=None, extension=None):
            super().__init__(flowchart=flowchart, title="Cubic", extension=extension)

        @property
        def version(self):
            return "0.1"

        def description_text(self, P=None):
            return self.header + "\\n    A cubic crystal."

        def run(self):
            next_node = super().run(None)
            db = self.get_variable("_system_db")
            system = db.create_system(name="argon")
            configuration = system.create_configuration(
                name="cubic", periodicity=3, coordinate_system="Cartesian"
            )
            configuration.cell.parameters = [3.0, 3.0, 3.0, 90.0, 90.0, 90.0]
            configuration.atoms.append(x=[0.0], y=[0.0], z=[0.0], symbol=["Ar"])
            db.system = system
            return next_node


    class CubicStep:
        my_description = {
            "description": "A cubic crystal for tests",
            "group": "Building",
            "name": "Cubic",
        }

        def __init__(self, flowchart=None, gui=None):
            pass

        def description(self):
            return CubicStep.my_description

        def create_node(self, flowchart=None, **kwargs):
            return Cubic(flowchart=flowchart, **kwargs)

        def create_tk_node(self, canvas=None, **kwargs):
            raise NotImplementedError("no GUI for the test step")
''')


def test_choices_and_defaults():
    P = StrainParameters()
    handling = P["structure handling"]
    assert handling.value == "Create a new configuration"
    assert tuple(handling.enumeration) == (
        "Overwrite the current configuration",
        "Create a new configuration",
        "Create a new system and configuration",
    )
    assert "subsequent structure handling" not in P
    assert P["configuration name"].value == STRAIN_NAME
    assert P["system name"].value == "keep current name"


@pytest.mark.parametrize(
    "old, new",
    [
        ("be put in a new configuration", "Create a new configuration"),
        ("overwrite the current configuration", "Overwrite the current configuration"),
    ],
)
def test_old_flowcharts_translated(old, new):
    """Flowcharts saved by earlier versions hold the old spellings."""
    P = StrainParameters(data={"structure handling": {"value": old}})
    assert P["structure handling"].value == new


def run_strain(tmp_path, **parameters):
    testing = pytest.importorskip("seamm_exec.testing")
    site = tmp_path / "cubic_site"
    info = site / "seamm_test_cubic-0.1.dist-info"
    info.mkdir(parents=True)
    (site / "seamm_test_cubic.py").write_text(CUBIC_STEP)
    (info / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: seamm-test-cubic\nVersion: 0.1\n"
    )
    (info / "entry_points.txt").write_text(
        "[org.molssi.seamm]\nCubic = seamm_test_cubic:CubicStep\n\n"
        "[org.molssi.seamm.tk]\nCubic = seamm_test_cubic:CubicStep\n"
    )
    lines = "".join(f"        {k}: '{v}'\n" for k, v in parameters.items())
    spec = (
        "title: Strain test\nsteps:\n- Cubic: {}\n- Strain:\n"
        + "        strain_xx: '0.01'\n"
        + lines
    )
    job = testing.run_spec(tmp_path, spec, source=SOURCE, extra_path=[site])
    db = sqlite3.connect(f"file:{job / 'seamm.db'}?mode=ro", uri=True)
    try:
        systems = db.execute("SELECT id, name FROM system ORDER BY id").fetchall()
        configurations = db.execute(
            "SELECT id, system, name, cell FROM configuration ORDER BY id"
        ).fetchall()
        cells = dict(
            (row[0], row[1:])
            for row in db.execute("SELECT id, a, b, c FROM cell").fetchall()
        )
    finally:
        db.close()
    return job, systems, configurations, cells


def test_new_configuration_named_by_the_strain(tmp_path):
    job, systems, configurations, cells = run_strain(tmp_path)
    assert [name for _, name in systems] == ["argon"]
    first, second = configurations
    assert first[2] == "cubic" and second[2] == "strained by (0.01, 0, 0, 0, 0, 0)"
    assert cells[first[3]][0] == pytest.approx(3.0)  # the original is untouched
    assert cells[second[3]][0] == pytest.approx(3.03)
    assert cells[second[3]][1] == pytest.approx(3.0)


def test_overwrite_the_current_configuration(tmp_path):
    job, systems, configurations, cells = run_strain(
        tmp_path,
        **{
            "structure handling": "Overwrite the current configuration",
            "configuration name": "keep current name",
        },
    )
    assert len(systems) == 1 and len(configurations) == 1
    (only,) = configurations
    assert only[2] == "cubic"
    assert cells[only[3]][0] == pytest.approx(3.03)
    # The table shows the cell before and after, not the strained one twice
    out = (job / "2" / "step.out").read_text()
    cells_table = [line.split("|") for line in out.splitlines() if line.count("|") >= 4]
    (row,) = [cells for cells in cells_table if cells[1].strip() == "a"]
    initial, final = (float(c) for c in row[2:4])
    assert initial == pytest.approx(3.0) and final == pytest.approx(3.03)


def test_new_system_and_configuration(tmp_path):
    job, systems, configurations, cells = run_strain(
        tmp_path,
        **{
            "structure handling": "Create a new system and configuration",
            "system name": "strained argon",
        },
    )
    assert [name for _, name in systems] == ["argon", "strained argon"]
    assert configurations[-1][1] == systems[-1][0]
    assert cells[configurations[-1][3]][0] == pytest.approx(3.03)
