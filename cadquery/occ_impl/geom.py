"""Geometry primitives and transformations for CadQuery.

This module provides core geometric types including vectors, matrices,
planes, and bounding boxes used throughout the CadQuery library.
"""

import math
from typing import Optional, Tuple, Union, overload

from OCP.gp import (
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Dir,
    gp_Pnt,
    gp_Trsf,
    gp_Vec,
)
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib


class Vector:
    """A 3D vector with common geometric operations.

    Wraps the OCC gp_Vec and gp_Pnt types to provide a convenient
    Python interface for vector math.

    Examples:
        >>> v = Vector(1, 2, 3)
        >>> v.length()
        3.7416573867739413
        >>> v.normalized()
        Vector(0.267, 0.535, 0.802)
    """

    def __init__(self, *args):
        if len(args) == 3:
            self._wrapped = gp_Vec(args[0], args[1], args[2])
        elif len(args) == 2:
            # 2-arg form assumes Z=0, useful for 2D work
            self._wrapped = gp_Vec(args[0], args[1], 0.0)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (list, tuple)):
                self._wrapped = gp_Vec(*arg)
            elif isinstance(arg, gp_Vec):
                self._wrapped = arg
            elif isinstance(arg, gp_Pnt):
                self._wrapped = gp_Vec(arg.X(), arg.Y(), arg.Z())
            elif isinstance(arg, gp_Dir):
                self._wrapped = gp_Vec(arg)
            else:
                raise TypeError(f"Cannot construct Vector from {type(arg)}")
        elif len(args) == 0:
            self._wrapped = gp_Vec(0.0, 0.0, 0.0)
        else:
            raise TypeError(f"Vector accepts 0-3 arguments, got {len(args)}")

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def length(self) -> float:
        """Return the magnitude of this vector."""
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._wrapped.Normalized())

    def dot(self, other: "Vector") -> float:
        """Compute the dot product with another vector."""
        return self._wrapped.Dot(other._wrapped)

    def cross(self, other: "Vector") -> "Vector":
        """Compute the cross product with another vector."""
        return Vector(self._wrapped.Crossed(other._wrapped))

    def distance_to(self, other: "Vector") -> float:
        """Return the Euclidean distance to another vector."""
        return self.to_pnt().Distance(other.to_pnt())

    def to_pnt(self) -> gp_Pnt:
        """Convert to an OCC gp_Pnt."""
        return gp_Pnt(self.x, self.y, self.z)

    def to_dir(self) -> gp_Dir:
        """Convert to an OCC gp_Dir (unit direction)."""
        return gp_Dir(self._wrapped)

    def __add__(self, other: "Vector") -> "Vector":
        """Add two vectors together."""
        return Vector(self._wrapped.Added(other._wrapped))

    def __sub__(self, other: "Vector") -> "Vector":
        """Subtract another vector from this one."""
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def __mul__(self, scalar: float) -> "Vector":
        """Multiply this vector by a scalar."""
        return Vector(self._wrapped.Multiplied(scalar))

    def __repr__(self) -> str:
        """Return a readable string representation of the vector."""
        return f"Vector({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
