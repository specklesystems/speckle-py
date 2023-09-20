from typing import Any, Dict, List, Union, Optional
from specklepy.objects.base import Base
from specklepy.objects.other import Collection

from specklepy.objects.GIS.CRS import CRS
from deprecated import deprecated


@deprecated(version="2.15", reason="Use VectorLayer or RasterLayer instead")
class Layer(Base, detachable={"features"}):
    """A GIS Layer"""

    def __init__(
        self,
        name: str = None,
        crs: CRS = None,
        units: str = "m",
        features: Optional[List[Base]] = None,
        layerType: str = "None",
        geomType: str = "None",
        renderer: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.crs = crs
        self.units = units
        self.type = layerType
        self.features = features or []
        self.geomType = geomType
        self.renderer = renderer or {}


class VectorLayer(
    Collection,
    detachable={"elements"},
    speckle_type="Objects.GIS.VectorLayer",
    serialize_ignore={"features"},
    speckle_type_translations={"VectorLayer": "Objects.GIS.VectorLayer"},
):

    """GIS Vector Layer"""

    name: Optional[str] = None
    crs: Optional[Union[CRS, Base]] = None
    units: Optional[str] = None
    elements: Optional[List[Base]] = None
    attributes: Optional[Base] = None
    geomType: Optional[str] = "None"
    renderer: Optional[Dict[str, Any]] = None
    collectionType = "VectorLayer"

    @property
    @deprecated(version="2.14", reason="Use elements")
    def features(self) -> Optional[List[Base]]:
        return self.elements

    @features.setter
    def features(self, value: Optional[List[Base]]) -> None:
        self.elements = value


class RasterLayer(
    Collection,
    detachable={"elements"},
    speckle_type="Objects.GIS.RasterLayer",
    serialize_ignore={"features"},
    speckle_type_translations={"RasterLayer": "Objects.GIS.RasterLayer"},
):

    """GIS Raster Layer"""

    name: Optional[str] = None
    crs: Optional[Union[CRS, Base]] = None
    units: Optional[str] = None
    rasterCrs: Optional[Union[CRS, Base]] = None
    elements: Optional[List[Base]] = None
    geomType: Optional[str] = "None"
    renderer: Optional[Dict[str, Any]] = None
    collectionType = "RasterLayer"

    @property
    @deprecated(version="2.14", reason="Use elements")
    def features(self) -> Optional[List[Base]]:
        return self.elements

    @features.setter
    def features(self, value: Optional[List[Base]]) -> None:
        self.elements = value
