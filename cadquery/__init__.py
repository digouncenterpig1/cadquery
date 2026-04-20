"""CadQuery - A parametric 3D CAD scripting framework built on top of OCCT."""

# Personal fork - using this for learning CadQuery and building custom parts
# Fork started: tracking upstream 2.4.0 release
# Upstream: https://github.com/CadQuery/cadquery

from .cq import (
    CQContext,
    CadQuery,
    Workplane,
)
from .occ_impl.geom import Vector, Matrix, Plane, Location
from .occ_impl.shapes import (
    Shape,
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Compound,
)
from .assembly import Assembly, Constraint
from .selectors import (
    Selector,
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    RadiusNthSelector,
    CenterNthSelector,
    DirectionNthSelector,
    LengthNthSelector,
    AreaNthSelector,
    StringSyntaxSelector,
)
from .exporters import exporters
from . import importers

__version__ = "2.4.0"

# Handy shorthand alias - I always type cq.WP instead of cq.Workplane anyway
WP = Workplane

__all__ = [
    "CQContext",
    "CadQuery",
    "Workplane",
    "WP",
    "Vector",
    "Matrix",
    "Plane",
    "Location",
    "Shape",
    "Vertex",
    "Edge",
    "Wire",
    "Face",
    "Shell",
    "Solid",
    "Compound",
    "Assembly",
    "Constraint",
    "Selector",
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "RadiusNthSelector",
    "CenterNthSelector",
    "DirectionNthSelector",
    "LengthNthSelector",
    "AreaNthSelector",
    "StringSyntaxSelector",
    "exporters",
    "importers",
]
