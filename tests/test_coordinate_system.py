#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 18:26:08 2018

@author: magdalenakrzus
"""
import numpy as np
from kristal.geometry.equiv import SkewCoordinateSystem

def test_cartesian_system():
    """SkewCoordinateSystem should act as Cartesian one for straight angles nad unit lengths."""
    system = SkewCoordinateSystem(1, 1, 1, np.pi / 2, np.pi / 2, np.pi / 2)
    assert np.allclose(system.change_of_basis_matrix(), np.eye(3))
    assert np.allclose(system.inv_change_of_basis_matrix(), np.eye(3))
