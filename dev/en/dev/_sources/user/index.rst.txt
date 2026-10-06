User Documentation
==================

At the moment this is a very simple plug-in: you provide strains in Voigt notation,
i.e. there are six independent strains. When run, the system is strained as requested
and the atoms move affinely with the change in the cell, i.e. the fractional coordinates
are unchanged. If you stretch the cell, the atoms move apart uniformly. If you compress
the cell, the atoms move together uniformly.

The strained structure can overwrite the current configuration, be added as a new
configuration of the current system (the default), or be put in a new system, as in
SEAMM's other steps that make structures. A new configuration is named after the
strains, e.g. ``strained by (0.01, 0, 0, 0, 0, 0)``, unless you choose another name;
the system's name is asked for only when a new system is made. A system that is not
periodic is left as it is, and the flowchart carries on.

In the future this plug-in could have added options to allow keeping molecules unchanged
by moving their center of mass or geometry. This could be useful for fluid systems, for
example.

..
    <remove the dots above and this line and unindent the toctree to expose it>
    Contents:

    .. toctree::
       :glob:
       :maxdepth: 2
       :titlesonly:

       *

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
