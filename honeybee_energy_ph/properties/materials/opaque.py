# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.material.opaque.EnergyMaterial Objects"""


from collections import defaultdict

try:
    from typing import Any, Iterable, List, NoReturn, Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_energy.material import opaque
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy:\n\t{}".format(e))

try:
    from honeybee_ph_utils.color import PhColor
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_utils:\n\t{}".format(e))


class CellPositionError(Exception):
    """An error for when a cell position is out of range."""

    def __init__(self, msg):
        super(CellPositionError, self).__init__(msg)


class PhDivisionCell(object):
    """A single cell in a PhLayerDivisionGrid."""

    def __init__(self, _row, _column, _hbe_material):
        # type: (int, int, opaque.EnergyMaterial) -> None
        self.row = _row
        self.column = _column
        self.material = _hbe_material

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}
        d["row"] = self.row
        d["column"] = self.column
        d["material"] = self.material.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhDivisionCell
        new_cell = cls(
            _input_dict["row"], _input_dict["column"], opaque.EnergyMaterial.from_dict(_input_dict["material"])
        )
        return new_cell

    def duplicate(self):
        # type: () -> PhDivisionCell
        """Duplicate the cell."""
        return PhDivisionCell(self.row, self.column, self.material.duplicate())

    def __copy__(self):
        # type: () -> PhDivisionCell
        return self.duplicate()

    def __str__(self):
        return "{}(row={}, column={}, material={})".format(
            self.__class__.__name__,
            self.row,
            self.column,
            self.material.display_name,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhDivisionGrid(object):
    """A grid of PhDivisionCell to support 'mixed' materials.

    The Cell grid is ordered from top-left to bottom-right:

    |    | C0  | C1  | C2  | ...
    |:---|:---:|:---:|:---:|:---:
    | R0 | 0,0 | 1,0 | 2,0 | ...
    | R1 | 0,1 | 1,1 | 2,1 | ...
    | R2 | 0,2 | 1,2 | 2,2 | ...
    """

    def __init__(self):
        # type: () -> None
        self._row_heights = []  # type: List[float]
        self._column_widths = []  # type: List[float]
        self._cells = []  # type: List[PhDivisionCell]

    @property
    def column_widths(self):
        # type: () -> List[float]
        """Return the list of column widths."""
        return self._column_widths

    @property
    def column_count(self):
        # type: () -> int
        """Return the number of columns in the grid."""
        return len(self._column_widths)

    @property
    def row_heights(self):
        # type: () -> List[float]
        """Return the list of row heights."""
        return self._row_heights

    @property
    def row_count(self):
        # type: () -> int
        """Return the number of rows in the grid."""
        return len(self._row_heights)

    @property
    def cell_count(self):
        # type: () -> int
        """Return the total number of cells in the grid."""
        return self.row_count * self.column_count

    @property
    def cells(self):
        # type: () -> List[PhDivisionCell]
        """Return the list of all the cells in the grid, sorted by row/column."""
        return sorted(self._cells, key=lambda x: (x.row, x.column))

    def set_column_widths(self, _column_widths):
        # type: (Iterable[float]) -> None
        """Set the column widths of the grid."""
        self._column_widths = []
        for width in _column_widths:
            self.add_new_column(width)

    def add_new_column(self, _column_width):
        # type: (float) -> None
        """Add a new COLUMN to the grid with the given width."""
        if _column_width is None:
            return

        if _column_width > 0:
            self._column_widths.append(float(_column_width))

    def set_row_heights(self, _row_heights):
        # type: (Iterable[float]) -> None
        """Set the row heights of the grid."""
        self._row_heights = []
        for height in _row_heights:
            self.add_new_row(height)

    def add_new_row(self, _row_height):
        # type: (float) -> None
        """Add a new ROW to the grid with the given height."""
        if _row_height is None:
            return

        if _row_height > 0:
            self._row_heights.append(float(_row_height))

    def get_cell(self, _column, _row):
        # type: (int, int) -> Optional[PhDivisionCell]
        """Get the PhDivisionCell at the given column and row position."""
        for cell in self._cells:
            if cell.column == _column and cell.row == _row:
                return cell
        return None

    def set_cell_material(self, _column_num, _row_num, _hbe_material):
        # type: (int, int, opaque.EnergyMaterial) -> None
        """Set the EnergyMaterial for a specific cell in the grid by its column/row position.

        Cells are indexed by their column and row position stating from top-left:

        |   | C0   | C1  | C2  | ...
        |---|------|-----|-----|----
        |R0 | 0,0  | 1,0 | 2,0 | ...
        |R1 | 0,1  | 1,1 | 2,1 | ...
        |R2 | 0,2  | 1,2 | 2,2 | ...
        """
        if _column_num >= self.column_count:
            msg = (
                "Error setting Material '{}' to column '{}'. The specified column is out of range. "
                "Please setup all the column-widths before assigning any materials. And "
                "remember that the columns start counting from '0', not '1'.".format(
                    _hbe_material.display_name, _column_num
                )
            )
            raise CellPositionError(msg)

        if _row_num >= self.row_count:
            msg = (
                "Error setting Material '{}' to row '{}'. The specified row is out of range. "
                "Please setup all the row-heights before assigning any materials. And "
                "remember that the rows start counting from '0', not '1'.".format(_hbe_material.display_name, _row_num)
            )
            raise CellPositionError(msg)

        # -- See if the cell already exists, if so reset its material
        # -- if it does not exist, create a new cell.
        existing_cell = self.get_cell(_column_num, _row_num)
        if existing_cell:
            existing_cell.material = _hbe_material
        else:
            new_cell = PhDivisionCell(_row=_row_num, _column=_column_num, _hbe_material=_hbe_material)
            self._cells.append(new_cell)

    def get_cell_material(self, _column_num, _row_num):
        # type: (int, int) -> Optional[opaque.EnergyMaterial]
        """Get the PhxMaterial for a specific cell in the grid by its column/row position."""
        for cell in self._cells:
            if cell.row == _row_num and cell.column == _column_num:
                return cell.material
        return None

    def get_cell_area(self, _column_num, _row_num):
        # type: (int, int) -> float
        """Get the area of a specific cell in the grid by its column/row position."""
        if _column_num >= self.column_count:
            return 0.0
        if _row_num >= self.row_count:
            return 0.0
        return self._column_widths[_column_num] * self._row_heights[_row_num]

    def get_base_material(self):
        # type: () -> Optional[opaque.EnergyMaterial]
        """Returns the 'base' material (the most common material in the grid, by area)."""
        if not self._cells:
            return None

        # -- Collect all the cell areas
        material_areas = defaultdict(float, default=0.0)
        for cell in self.cells:
            cell_area = self.get_cell_area(cell.column, cell.row)
            material_areas[cell.material.identifier] += cell_area

        # -- Find the material with the largest area. This is the 'base' material
        base_material_id = sorted(material_areas.items(), key=lambda x: x[1])[-1][0]
        for cell in self.cells:
            if cell.material.identifier == base_material_id:
                return cell.material

        return None

    def get_equivalent_conductivity(self):
        # type: () -> float
        """Return an area-weighted average of the conductivities of all materials in the grid."""
        total_area = 0.0
        total_conductivity = 0.0
        for cell in self.cells:
            cell_area = self.get_cell_area(cell.column, cell.row)
            total_area += cell_area
            total_conductivity += cell_area * cell.material.conductivity

        if total_area > 0:
            return total_conductivity / total_area
        return 0.0

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}
        d["column_widths"] = self.column_widths
        d["row_heights"] = self.row_heights
        d["cells"] = []
        for cell in self._cells:
            d["cells"].append(cell.to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhDivisionGrid
        new_grid = cls()
        new_grid.set_column_widths(_input_dict.get("column_widths", []))
        new_grid.set_row_heights(_input_dict.get("row_heights", []))
        for cell_dict in _input_dict.get("cells", []):
            new_grid.set_cell_material(
                cell_dict["column"],
                cell_dict["row"],
                opaque.EnergyMaterial.from_dict(cell_dict["material"]),
            )
        return new_grid

    def duplicate(self):
        # type: () -> PhDivisionGrid
        """Duplicate the grid."""
        new_grid = PhDivisionGrid()
        new_grid.set_column_widths(self.column_widths)
        new_grid.set_row_heights(self.row_heights)
        for cell in self._cells:
            new_grid.set_cell_material(cell.column, cell.row, cell.material.duplicate())
        return new_grid

    def __copy__(self):
        # type: () -> PhDivisionGrid
        return self.duplicate()

    def __str__(self):
        return "{}(columns={}, rows={})".format(
            self.__class__.__name__,
            self.column_count,
            self.row_count,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialPhProperties(object):
    """Passive House properties for EnergyMaterial objects."""

    def __init__(self, _host=None):
        # type: (Optional[opaque.EnergyMaterial]) -> None
        self._host = _host
        self.id_num = 0
        self._ph_color = None  # type: Optional[PhColor]
        self.user_data = {}
        self.base_material = None  # type: Optional[opaque.EnergyMaterial]
        self.divisions = PhDivisionGrid()

    # -------------------------------------------------------------------------
    # ------------------ Deprecated [April 4, 2024] ---------------------------

    @property
    def percentage_of_assembly(self):
        # type: () -> NoReturn
        raise DeprecationWarning(
            "The 'percentage_of_assembly' property is deprecated. Please use the 'divisions' for mixed materials."
        )

    @percentage_of_assembly.setter
    def percentage_of_assembly(self, _percentage):
        # type: (Any) -> NoReturn
        raise DeprecationWarning(
            "The 'percentage_of_assembly' property is deprecated. Please use the 'divisions' for mixed materials."
        )

    @property
    def base_materials(self):
        # type: () -> NoReturn
        raise DeprecationWarning(
            "The 'base_materials' property is deprecated. Please use the 'divisions' for mixed materials."
        )

    @base_materials.setter
    def base_materials(self, _materials):
        # type: (Any) -> NoReturn
        raise DeprecationWarning(
            "The 'base_materials' property is deprecated. Please use the 'divisions' for mixed materials."
        )

    def add_base_material(self, _hb_material):
        # type: (Any) -> NoReturn
        raise DeprecationWarning(
            "The 'add_base_material' function is deprecated. Please use the 'divisions' for mixed materials."
        )

    def clear_base_materials(self):
        # type: (Any) -> NoReturn
        raise DeprecationWarning(
            "The 'clear_base_materials' function is deprecated. Please use the 'divisions' for mixed materials."
        )

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    @property
    def ph_color(self):
        # type: () -> Optional[PhColor]
        return self._ph_color

    @ph_color.setter
    def ph_color(self, _input_color):
        # type: (Optional[PhColor]) -> None
        self._ph_color = _input_color

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d["id_num"] = self.id_num
        d["divisions"] = self.divisions.to_dict()
        d["user_data"] = self.user_data

        if self.ph_color:
            d["ph_color"] = self.ph_color.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Optional[opaque.EnergyMaterial]) -> EnergyMaterialPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop._ph_color = PhColor.from_dict(_input_dict.get("ph_color", None))
        new_prop.user_data = _input_dict.get("user_data", {})
        new_prop.divisions = PhDivisionGrid.from_dict(_input_dict.get("divisions", {}))
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        # type: (Any) -> None
        return None

    def __copy__(self, new_host=None):
        # type: (Optional[opaque.EnergyMaterial]) -> EnergyMaterialPhProperties
        _host = new_host or self._host
        new_obj = EnergyMaterialPhProperties(_host)
        new_obj.id_num = self.id_num
        new_obj.divisions = self.divisions.duplicate()
        new_obj.user_data = self.user_data.copy()
        if self.ph_color:
            new_obj.ph_color = self.ph_color.duplicate()
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Optional[opaque.EnergyMaterial]) -> EnergyMaterialPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, ph_color={!r})".format(
            self.__class__.__name__,
            self.id_num,
            self.ph_color,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialNoMassPhProperties(object):
    def __init__(self, _host=None):
        # type: (Optional[opaque.EnergyMaterialNoMass]) -> None
        self.host = _host
        self.id_num = 0
        self._ph_color = None  # type: Optional[PhColor]
        self.user_data = {}
        self.divisions = None

    @property
    def ph_color(self):
        # type: () -> Optional[PhColor]
        return self._ph_color

    @ph_color.setter
    def ph_color(self, _input_color):
        # type: (Optional[PhColor]) -> None
        self._ph_color = _input_color

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d["id_num"] = self.id_num
        d["user_data"] = self.user_data
        d["divisions"] = self.divisions

        if self.ph_color:
            d["ph_color"] = self.ph_color.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Optional[opaque.EnergyMaterialNoMass]) -> EnergyMaterialNoMassPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop._ph_color = PhColor.from_dict(_input_dict.get("ph_color", None))
        new_prop.user_data = _input_dict.get("user_data", {})
        new_prop.divisions = _input_dict["divisions"]
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        # type: (dict) -> None
        return

    def __copy__(self, new_host=None):
        # type: (Optional[opaque.EnergyMaterialNoMass]) -> EnergyMaterialNoMassPhProperties
        _host = new_host or self.host
        new_obj = EnergyMaterialNoMassPhProperties(_host)
        new_obj.id_num = self.id_num
        new_obj.user_data = self.user_data.copy()
        new_obj.divisions = self.divisions
        if self.ph_color:
            new_obj.ph_color = self.ph_color.duplicate()
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Optional[opaque.EnergyMaterialNoMass]) -> EnergyMaterialNoMassPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, ph_color={!r})".format(self.__class__.__name__, self.id_num, self.ph_color)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialVegetationPhProperties(object):
    def __init__(self, _host=None):
        # type: (Optional[opaque.EnergyMaterialVegetation]) -> None
        self.host = _host
        self.id_num = 0
        self._ph_color = None  # type: Optional[PhColor]
        self.user_data = {}
        self.divisions = None

    @property
    def ph_color(self):
        # type: () -> Optional[PhColor]
        return self._ph_color

    @ph_color.setter
    def ph_color(self, _input_color):
        # type: (Optional[PhColor]) -> None
        self._ph_color = _input_color

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d["id_num"] = self.id_num
        d["user_data"] = self.user_data
        d["divisions"] = self.divisions

        if self.ph_color:
            d["ph_color"] = self.ph_color.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict[str, Any], Optional[opaque.EnergyMaterialVegetation]) -> EnergyMaterialVegetationPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop._ph_color = PhColor.from_dict(_input_dict.get("ph_color", None))
        new_prop.user_data = _input_dict.get("user_data", {})
        new_prop.divisions = _input_dict["divisions"]
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Optional[opaque.EnergyMaterialVegetation]) -> EnergyMaterialVegetationPhProperties
        _host = new_host or self.host
        new_obj = EnergyMaterialVegetationPhProperties(_host)
        new_obj.id_num = self.id_num
        new_obj.user_data = self.user_data.copy()
        new_obj.divisions = self.divisions
        if self.ph_color:
            new_obj.ph_color = self.ph_color.duplicate()
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Optional[opaque.EnergyMaterialVegetation]) -> EnergyMaterialVegetationPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, ph_color={!r})".format(self.__class__.__name__, self.id_num, self.ph_color)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
