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
    """

    def __init__(self, *args):
        if len(args) == 3:
            self._wrapped = gp_Vec(args[0], args[1], args[2])
        elif len(args) == 2:
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
        return Vector(self._wrapped.Added(other._wrapped))

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scalar))

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        return Vector(self._wrapped.Reversed())

    def __repr__(self) -> str:
        return f"Vector({self.x:.6g}, {self.y:.6g}, {self.z:.6g})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self._wrapped.IsEqual(other._wrapped, 1e-9, 1e-9)


class BoundingBox:
    """Axis-aligned bounding box."""

    def __init__(self, bb: Optional[Bnd_Box] = None):
        if bb is None:
            self._bbox = Bnd_Box()
        else:
            self._bbox = bb

        self.xmin, self.ymin, self.zmin = 0.0, 0.0, 0.0
        self.xmax, self.ymax, self.zmax = 0.0, 0.0, 0.0

        if not self._bbox.IsVoid():
            self.xmin, self.ymin, self.zmin, self.xmax, self.ymax, self.zmax = (
                self._bbox.Get()
            )

    @property
    def center(self) -> Vector:
        """Return the center point of the bounding box."""
        return Vector(
            (self.xmin + self.xmax) / 2.0,
            (self.ymin + self.ymax) / 2.0,
            (self.zmin + self.zmax) / 2.0,
        )

    @property
    def diagonal_length(self) -> float:
        """Return the length of the space diagonal."""
        return math.sqrt(
            (self.xmax - self.xmin) ** 2
            + (self.ymax - self.ymin) ** 2
            + (self.zmax - self.zmin) ** 2
        )

    def is_inside(self, point: Vector) -> bool:
        """Check whether a point lies within the bounding box."""
        return (
            self.xmin <= point.x <= self.xmax
            and self.ymin <= point.y <= self.ymax
            and self.zmin <= point.z <= self.zmax
        )

    def __repr__(self) -> str:
        return (
            f"BoundingBox(x=[{self.xmin:.4g}, {self.xmax:.4g}], "
            f"y=[{self.ymin:.4g}, {self.ymax:.4g}], "
            f"z=[{self.zmin:.4g}, {self.zmax:.4g}])"
        )
