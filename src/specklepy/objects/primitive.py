from dataclasses import dataclass

from specklepy.objects.base import Base


@dataclass(kw_only=True)
class Interval(Base, speckle_type="Objects.Primitive.Interval", serialize_ignore={"length"}):
    start: float = 0.0
    end: float = 0.0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(start: {self.start}, end: {self.end})"

    @property
    def length(self) -> float:
        return self.__dict__.get('_length')

    @length.setter
    def length(self, value: float) -> None:
        self.__dict__['_length'] = value

    def calculate_length(self) -> float:
        return abs(self.end - self.start)

    @classmethod
    def unit_interval(cls) -> "Interval":
        interval = cls(start=0, end=1)
        interval.length = interval.calculate_length()
        return interval
