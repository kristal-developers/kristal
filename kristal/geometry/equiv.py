# -*- coding: utf-8 -*-
"""Various utilities for working with atoms' equivalence positions."""
import numpy as np
from numpy import sin, cos

def cos2(x):
    """Shortcut for computing :code:`np.cos(x) ** 2`."""
    return cos(x) ** 2

def sin2(x):
    """Shortcut for computing :code:`np.sin(x) ** 2`."""
    return sin(x) ** 2

class SkewCoordinateSystem(object):
    """Class representing fractional coordinates system.

    :ivar a: length of first periodic vector.
    :vartype a: float
    :ivar b: length of second periodic vector.
    :vartype b: float
    :ivar c: length of second periodic vector.
    :vartype c: float
    :ivar alpha: an angle between second and third periodic vector.
    :vartype alpha: float
    :ivar beta: an angle between first and third periodic vector.
    :vartype beta: float
    :ivar gamma: an angle between first and second periodic vector.
    :vartype gamma: float
    :param a: length of first periodic vector.
    :type a: float
    :param b: length of second periodic vector.
    :type b: float
    :param c: length of second periodic vector.
    :type c: float
    :param alpha: an angle between second and third periodic vector.
    :type alpha: float
    :param beta: an angle between first and third periodic vector.
    :type beta: float
    :param gamma: an angle between first and second periodic vector.
    :type gamma: float
    """
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
        """Volume of the cell in this coordinates system.

        Volume of the unit cell is defined as a volume of parallelepiped
        determined by periodic vectors and is given by:

        .. math::
          V = abc \\sqrt{1 - \\cos^2(\\alpha) - \\cos^2(\\beta) - \\cos^2(\\gamma) + 2\\cos(\\alpha)\\cos(\\beta) \\cos(\\gamma)}
        """
        return (self.a * self.b * self.c *
                (1 - cos2(self.alpha) - cos2(self.beta) - cos2(self.gamma) +
                 2 * cos(self.alpha) * cos(self.beta) * cos(self.gamma)) ** 0.5)

    def change_of_basis_matrix(self):
        r"""Change of basis matrix from fractional to Cartesian coordinates.

        Let :math:`(u, v, w)` be components of arbitrary vector in fractional coordinates.
        Components of this vector in Cartesian coordinates are given by

        .. math::
          \begin{bmatrix} x \\ y \\ z \end{bmatrix} = M \cdot \begin{bmatrix} u \\ v \\ w \end{bmatrix}

        where :math:`M` is given by

        .. math::
          M = \begin{bmatrix}
            a & b \cos(\gamma) & c \cos(\beta) \\
            0 & b \sin(\gamma) & c \frac{\cos(\alpha) - \cos(\beta)\cos(\gamma)}{\sin(\gamma)} \\
            0 & 0 & \frac{V}{ab \sin(\gamma)}
          \end{bmatrix}

        This method returns :math:`M` from the above equation.
        """
        return np.array([
            [self.a, self.b * cos(self.gamma), self.c * cos(self.beta)],
            [0, self.b * sin(self.gamma), self.c * (cos(self.alpha) - cos(self.beta) * cos(self.gamma)) / sin(self.gamma)],
            [0, 0, self.unit_cell_volume / self.a / self.b / sin(self.gamma)]])

    def inv_change_of_basis_matrix(self):
        """"Matrix changing basis from this system to Cartesian.

        This is an inverse of a matrix :math:`M` returned by :py:func:`change_of_basis_matrix`.
        """
        return np.linalg.inv(self.change_of_basis_matrix())
