#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 12:44:19 2018

@author: magdalenakrzus
"""
import numpy as np
from numpy import sin, cos

def cos2(x):
    return cos(x) ** 2

def sin2(x):
    return sin(x) ** 2

class SkewCoordinateSystem(object):
    """Class representing skew coordinates system."""
    # pylint: disable=invalid-name
    def __init__(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    @property
    def unit_cell_volume(self):
        """Volume of the cell in this coordinates system."""
        return (self.a * self.b * self.c *
                (1 - cos2(self.alpha) - cos2(self.beta) - cos2(self.gamma) +
                 2 * cos(self.alpha) * cos(self.beta) * cos(self.gamma)) ** 0.5)

    def change_of_basis_matrix(self):
        """Matrix changing basis from Cartesian to this system."""
        return np.array([
            [self.a, self.b * cos(self.gamma), self.c * cos(self.beta)],
            [0, self.b * sin(self.gamma), self.c * (cos(self.alpha) - cos(self.beta) * cos(self.gamma)) / sin(self.gamma)],
            [0, 0, self.unit_cell_volume / self.a / self.b / sin(self.gamma)]])

    def inv_change_of_basis_matrix(self):
        """"Matrix changing basis from this system to Cartesian."""
        return np.linalg.inv(self.change_of_basis_matrix())
