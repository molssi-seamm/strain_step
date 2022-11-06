#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `strain_step` package."""

import pytest  # noqa: F401
import strain_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = strain_step.Strain()
    assert str(type(result)) == "<class 'strain_step.strain.Strain'>"
