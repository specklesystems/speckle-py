from dataclasses import dataclass, field
from typing import List, Tuple

from specklepy.objects.base import Base
from specklepy.objects.geometry.point import Point
from specklepy.objects.interfaces import ICurve, IHasUnits
from specklepy.objects.models.units import Units
from specklepy.objects.primitive import Interval


@dataclass(kw_only=True)
class Line(Base, IHasUnits, ICurve, speckle_type="Objects.Geometry.Line"):
    """
    a line defined by two points in 3D space
    """

    start: Point
    end: Point
    domain: Interval = field(default_factory=Interval.unit_interval)

    @property
    def length(self) -> float:
        """
        calculate the length of the line using Point's distance_to method
        """
        return self.start.distance_to(self.end)

    @property
    def _domain(self) -> Interval:
        return self.domain

    def to_list(self) -> List[float]:
        result = []
        result.extend(self.start.to_list())
        result.extend(self.end.to_list())
        result.extend([self.domain.start, self.domain.end])
        return result

    @classmethod
    def from_list(cls, coords: List[float], units: str | Units) -> "Line":
        if len(coords) < 6:
            raise ValueError(
                "Line from coordinate array requires 6 coordinates.")

        start = Point(x=coords[0], y=coords[1], z=coords[2], units=units)
        end = Point(x=coords[3], y=coords[4], z=coords[5], units=units)

        return cls(start=start, end=end, units=units)

    @classmethod
    def from_coords(
        cls,
        start_x: float,
        start_y: float,
        start_z: float,
        end_x: float,
        end_y: float,
        end_z: float,
        units: str,
    ) -> "Line":
        start = Point(x=start_x, y=start_y, z=start_z, units=units)
        end = Point(x=end_x, y=end_y, z=end_z, units=units)
        return cls(start=start, end=end, units=units)

    def transform_to(self, transform) -> Tuple[bool, "Line"]:
        """
        transform this line using the given transform by transforming its start and end points
        """
        success_start, transformed_start = self.start.transform_to(transform)
        success_end, transformed_end = self.end.transform_to(transform)

        if not (success_start and success_end):
            return False, self

        transformed = Line(
            start=transformed_start,
            end=transformed_end,
            domain=self.domain,
            units=self.units,
            applicationId=self.applicationId
        )
        return True, transformed
