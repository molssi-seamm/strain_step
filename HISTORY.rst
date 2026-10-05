=======
History
=======

2026.10.5 -- SEAMM's standard choices for the strained structure; bugfixes
    * The strained structure can overwrite the current configuration, go in a new
      configuration (the default, as before) or in a new system, with SEAMM's
      standard choices and names. A new configuration is named after the strains,
      e.g. "strained by (0.01, 0, 0, 0, 0, 0)" -- it was left unnamed -- and the
      system name is asked for only when a new system is made. Flowcharts saved with
      the earlier wording ("be put in a new configuration") are read as before.
    * Bugfix: when overwriting the current configuration, the table of the cell
      showed the strained cell as the initial one too.
    * Bugfix: a system that is not periodic ended the flowchart instead of being
      left as it is.
    * Builds again with Python 3.12 (an old ``versioneer.py`` no longer worked);
      requires seamm 2026.10.3.

2022.11.7 -- Initial release
  First version, which handles straining systems moving the atoms affinely.
