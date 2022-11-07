User Documentation
==================

At the moment this is a very simple plug-in: you provide strains in Voigt notation,
i.e. there are six independent strains. When run, the system is strained as requested
and the atoms move affinely with the change in the cell, i.e. the fractional coordinates
are unchanged. If you stretch the cell, the atoms move apart uniformly. If you compress
the cell, the atoms move together uniformly.

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
