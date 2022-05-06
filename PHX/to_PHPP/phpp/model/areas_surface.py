# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a PHPP Areas / Surface-Entry row"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, ClassVar, Dict
from functools import partial

from PHX.model import building, geometry
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceType

from PHX.to_PHPP.phpp import xl_data


@dataclass
class SurfaceRow:
    """A single Areas/Surface entry row."""

    columns: ClassVar[Dict] = {
        'description': 'L',
        'group_number': 'M',
        'quantity': 'P',
        'area': 'V',
        'assembly_id': 'AC',
        'orientation': 'AG',
        'angle': 'AH',
        'shading': 'AJ',
        'absorptivity': 'AK',
        'emissivity': 'AL',
    }

    __slots__ = ('phx_polygon', 'phx_component', 'phpp_assembly_id_name')
    phx_polygon: geometry.PhxPolygon
    phx_component: building.PhxComponent
    phpp_assembly_id_name: Optional[str]

    @property
    def phpp_group_number(self) -> int:
        if self.phx_component.face_type == ComponentFaceType.WALL:
            if self.phx_component.exposure_exterior == ComponentExposureExterior.EXTERIOR:
                return 8
            else:
                return 9
        elif self.phx_component.face_type == ComponentFaceType.FLOOR:
            return 11
        elif self.phx_component.face_type == ComponentFaceType.ROOF_CEILING:
            return 10
        else:
            return 12

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

    def create_xl_items(self, _sheet_name: str, _row_num: int) -> List[xl_data.XlItem]:
        """Returns a list of the XL Items to write for this Surface Entry

        Arguments:
        ----------
            * _sheet_name: (str) The name of the worksheet to write to.
            * _row_num: (int) The row number to build the XlItems for
        Returns:
        --------
            * (List[XlItem]): The XlItems to write to the sheet.
        """
        create_range = partial(self._create_range, _row_num=_row_num)
        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('description'), self.phx_polygon.display_name),
            (create_range('group_number'), self.phpp_group_number),
            (create_range('quantity'),  1),
            (create_range('area'),  self.phx_polygon.area),
            (create_range('assembly_id'), self.phpp_assembly_id_name),
            (create_range('orientation'), self.phx_polygon.cardinal_orientation_angle),
            (create_range('angle'),  self.phx_polygon.angle_from_horizontal),
            (create_range('shading'),  0.5),
            (create_range('absorptivity'),  0.6),
            (create_range('emissivity'),  0.9),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
