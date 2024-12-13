from dataclasses import dataclass
from typing import List
from specklepy.objects.base import Base


@dataclass(kw_only=True)
class Interval(Base, speckle_type="Objects.Primitive.Interval"):
    start: float = 0.0  # Added default
    end: float = 0.0  # Added default

    @property
    def length(self) -> float:
        return abs(self.end - self.start)

    def __str__(self) -> str:
        return f"{super().__str__()}[{self.start}, {self.end}]"

    @classmethod
    def unit_interval(cls) -> "Interval":
        return cls(start=0, end=1)

    def to_list(self) -> List[float]:
        return [self.start, self.end]

    @classmethod
    def from_list(cls, args: List[float]) -> "Interval":
        return cls(start=args[0], end=args[1])
