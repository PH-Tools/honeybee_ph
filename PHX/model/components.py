# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Component (Face, Aperture) Classes"""

from __future__ import annotations
from typing import ClassVar, Collection, List, Set, Union

from PHX.model import geometry, constructions
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceType, ComponentFaceOpacity, ComponentColor


class PhxComponentBase:
    """Base class with id_num counter for Opaque and Aperture Components"""

    _count: ClassVar[int] = 0

    def __init__(self):
        PhxComponentBase._count += 1
        self._id_num: int = PhxComponentBase._count

    @property
    def id_num(self) -> int:
        return self._id_num


class PhxComponentOpaque(PhxComponentBase):
    """Opaque surface components (wall, roof, floor)."""

    def __init__(self):
        super().__init__()

        self.display_name: str = ""
        self.face_type: ComponentFaceType = ComponentFaceType.WALL
        self.face_opacity: ComponentFaceOpacity = ComponentFaceOpacity.OPAQUE
        self.color_interior: ComponentColor = ComponentColor.EXT_WALL_INNER
        self.color_exterior: ComponentColor = ComponentColor.EXT_WALL_INNER
        self.exposure_exterior: ComponentExposureExterior = ComponentExposureExterior.EXTERIOR
        self.exposure_interior: int = 1
        self.interior_attachment_id: int = -1

        self.assembly: constructions.PhxConstructionOpaque = constructions.PhxConstructionOpaque()
        self.assembly_type_id_num: int = -1

        self.apertures: List[PhxComponentAperture] = []
        self.polygons: List[geometry.PhxPolygon] = []

    @property
    def polygon_ids(self) -> Set[int]:
        """Return a Set of all the Polygon-id numbers found in the Component's Polygon group."""
        return {polygon.id_num for polygon in self.polygons}

    @property
    def unique_key(self) -> str:
        """Returns a unique text key,. Useful for sorting / grouping / merging components."""
        return f'{self.face_type}-{self.face_opacity}-{self.exposure_interior}-{self.interior_attachment_id}-'\
            f'{self.exposure_exterior}-{self.assembly_type_id_num}'

    def add_polygons(self,
                     _input: Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]) -> None:
        """Adds a new Polygon or Polygons to the Component's collection.

        Arguments:
        ----------
            * _input (Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]): The polygon or
                polygons to add to the component's collection.

        Returns:
        --------
            * None
        """
        if not isinstance(_input, Collection):
            _input = (_input,)

        for polygon in _input:
            self.polygons.append(polygon)

    def __add__(self, other: PhxComponentOpaque) -> PhxComponentOpaque:
        """Merge with another Component into a single new Component.

        Arguments:
        ----------
            * other (PhxComponentOpaque): The other PhxComponentOpaque to merge with.

        Returns:
        --------
            * (PhxComponentOpaque): A new Component with attributes merged.
        """
        new_compo = self.__class__()
        for attr_name, attr_val in vars(self).items():
            if attr_name.startswith('_'):
                continue
            setattr(new_compo, attr_name, attr_val)

        new_compo.display_name = 'Merged_Component'
        new_compo.polygons = self.polygons + other.polygons
        for phx_aperture in new_compo.apertures:
            phx_aperture.host = new_compo
        for phx_aperture in other.apertures:
            new_compo.add_aperture(phx_aperture)

        return new_compo

    def add_aperture(self, _aperture: PhxComponentAperture) -> None:
        """Add a new child PhxComponentAperture to the Component.

        Arguments:
        ----------
            * _aperture: (PhxComponentAperture): The new PhxComponentAperture to
                add as a child.
        Returns:
        --------
            * None
        """
        _aperture.host = self
        self.apertures.append(_aperture)

    def get_host_polygon_by_child_id_num(self, _id_num: int) -> geometry.PhxPolygon:
        """Return a single Polygon from the collection if it has the specified ID as a 'child'.

        If the specified ID number is not found, an Exception is raised.

        Arguments:
        ----------
            * _id_num: (int) The Polygon id-number to search the Component's collection for.
        Returns:
        -------
            * (PhxPolygon): The PhxPolygon with the specified id-number.
        """
        for polygon in self.polygons:
            if _id_num in polygon.child_polygon_ids:
                return polygon
        raise Exception(
            f'Error: Cannot find a host polygon for the child id_num: {_id_num}')


class PhxComponentAperture(PhxComponentBase):

    def __init__(self, _host: PhxComponentOpaque):
        super().__init__()

        self.host = _host

        self.display_name: str = ""
        self.face_type: ComponentFaceType = ComponentFaceType.WINDOW
        self.face_opacity: ComponentFaceOpacity = ComponentFaceOpacity.TRANSPARENT
        self.color_interior: ComponentColor = ComponentColor.WINDOW
        self.color_exterior: ComponentColor = ComponentColor.WINDOW
        self.exposure_exterior: ComponentExposureExterior = ComponentExposureExterior.EXTERIOR
        self.exposure_interior: int = 1
        self.interior_attachment_id: int = -1

        self.window_type: constructions.PhxConstructionWindow = constructions.PhxConstructionWindow()
        self.window_type_id_num: int = -1

        self.polygons: List[geometry.PhxPolygon] = []

    @property
    def polygon_ids(self) -> Set[int]:
        """Return a Set of all the Polygon-id numbers found in the Component's Polygon group."""
        return {polygon.id_num for polygon in self.polygons}

    @property
    def unique_key(self) -> str:
        """Returns a unique text key,. Useful for sorting / grouping / merging components."""
        return f'{self.face_type}-{self.face_opacity}-{self.exposure_interior}-{self.interior_attachment_id}-'\
            f'{self.exposure_exterior}-{self.window_type_id_num}'

    def add_polygons(self,
                     _input: Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]) -> None:
        """Adds a new Polygon or Polygons to the Component's collection.

        Arguments:
        ----------
            * _input (Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]): The polygon or
                polygons to add to the component's collection.

        Returns:
        --------
            * None
        """
        if not isinstance(_input, Collection):
            _input = (_input,)

        for polygon in _input:
            self.polygons.append(polygon)

    def __add__(self, other) -> PhxComponentAperture:
        """Merge with another Component into a single new Component.

        Arguments:
        ----------
            * other (PhxComponentAperture): The other PhxComponentAperture to merge with.

        Returns:
        --------
            * (PhxComponentAperture): A new Component with attributes merged.
        """
        new_compo = self.__class__(_host=self.host)
        for attr_name, attr_val in vars(self).items():
            if attr_name.startswith('_'):
                continue
            setattr(new_compo, attr_name, attr_val)

        new_compo.display_name = 'Merged_Component'
        new_compo.polygons = self.polygons + other.polygons

        return new_compo
