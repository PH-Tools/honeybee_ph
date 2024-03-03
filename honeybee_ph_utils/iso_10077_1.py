# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Calculate Window U-w as per ISO-10077-2:2006"""

import warnings

try:
    from ladybug_geometry.geometry3d import LineSegment3D, face
except ImportError as e:
    raise ImportError("Failed to import ladybug_geometry from ladybug_geometry.")

try:
    from honeybee import aperture
except ImportError as e:
    raise ImportError("Failed to import honeybee from honeybee.")

try:
    from honeybee_energy_ph.construction import window
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy_ph from honeybee_energy_ph.")


def get_ladybug_Face3D_width_and_height(_lbt_face3d):
    # type: (face.Face3D) -> tuple[float, float]
    """Get the width and height of a ladybug_geometry.geometry3d.face.Face3D object.

    If a non-rectangular object with more than 4 vertices is passed, a ValueError is raised.
    """

    if len(_lbt_face3d.vertices) != 4:
        raise ValueError(
            "The LBT-Face3D '{}' has {} vertices. Only use rectangular faces with 4 vertices.".format(
                _lbt_face3d, len(_lbt_face3d.vertices)
            )
        )

    (
        vertix_upper_left,
        vertix_upper_right,
        vertix_lower_right,
        vertix_lower_left,
    ) = _lbt_face3d.upper_left_counter_clockwise_vertices
    horizontal_edge = LineSegment3D.from_end_points(vertix_upper_left, vertix_upper_right)
    vertical_edge = LineSegment3D.from_end_points(vertix_upper_right, vertix_lower_right)

    height = horizontal_edge.length
    width = vertical_edge.length

    return width, height


def get_honeybee_aperture_width_and_height(_hb_aperture):
    # type: (aperture.Aperture) -> tuple[float, float]
    """Get the width and height of a rectangular honeybee.aperture.Aperture object.

    If a non-rectangular object with more than 4 vertices is passed, a ValueError is raised.
    """
    if len(_hb_aperture.geometry.vertices) != 4:
        raise ValueError(
            "The HB-Aperture '{}' has {} vertices. Only use rectangular Apertures with 4 vertices.".format(
                _hb_aperture.display_name, len(_hb_aperture.geometry.vertices)
            )
        )

    return get_ladybug_Face3D_width_and_height(_hb_aperture.geometry)


class ISO100771Data:
    """Wrapper class used to calculate the ISO-10077-1 heat-loss values."""

    def __init__(self, _win_width, _win_height, _frame, _glazing):
        # type: (float, float, window.PhWindowFrame, window.PhWindowGlazing) -> None
        self.win_width = _win_width
        self.win_height = _win_height
        self.frame = _frame
        self.glazing = _glazing

    @classmethod
    def from_hb_aperture(cls, _hb_aperture):
        # type: (aperture.Aperture) -> ISO100771Data
        """Create an ISO100771Data object from a honeybee.aperture.Aperture object."""

        hbe_prop = _hb_aperture.properties.energy  # type: ignore

        try:
            ph_frame = hbe_prop.construction.properties.ph.ph_frame
        except Exception as e:
            raise Exception("The Aperture does not have a PH-Style frame.", e)

        try:
            ph_glazing = hbe_prop.construction.properties.ph.ph_glazing
        except Exception as e:
            raise Exception("The Aperture does not have a PH-Style glazing.", e)

        (
            w,
            h,
        ) = get_honeybee_aperture_width_and_height(_hb_aperture)
        return cls(
            w,
            h,
            ph_frame,
            ph_glazing,
        )

    @classmethod
    def from_lbt_Face3D(cls, _hb_face3d, _ph_frame, _ph_glazing):
        # type: (face.Face3D, window.PhWindowFrame, window.PhWindowGlazing) -> ISO100771Data
        """Create an ISO100771Data object from a ladybug_geometry.geometry3d.face.Face3D object."""

        (
            w,
            h,
        ) = get_ladybug_Face3D_width_and_height(_hb_face3d)
        return cls(
            w,
            h,
            _ph_frame,
            _ph_glazing,
        )

    @property
    def area_window(self):
        # type: () -> float
        return self.side_exterior_length("right") * self.side_exterior_length("top")

    @property
    def area_glazing(self):
        # type: () -> float
        return self.side_interior_length("right") * self.side_interior_length("top")

    def side_interior_length(self, _side):
        # type: (str) -> float
        side_lengths = {
            "top": (self.win_width - self.frame.right.width - self.frame.left.width),
            "right": (self.win_height - self.frame.top.width - self.frame.bottom.width),
            "bottom": (self.win_width - self.frame.right.width - self.frame.left.width),
            "left": (self.win_height - self.frame.top.width - self.frame.bottom.width),
        }
        return side_lengths[_side]

    def side_exterior_length(self, _side):
        # type: (str) -> float
        side_lengths = {
            "top": self.win_width,
            "right": self.win_height,
            "bottom": self.win_width,
            "left": self.win_height,
        }
        return side_lengths[_side]

    def corner_area(self, _side):
        # type: (str) -> float
        """Correct for the overlap / 45 degrees at the corners"""

        adjacent_frames = {
            "top": {"adj_1": "left", "adj_2": "right"},
            "right": {"adj_1": "top", "adj_2": "bottom"},
            "bottom": {"adj_1": "left", "adj_2": "right"},
            "left": {"adj_1": "top", "adj_2": "bottom"},
        }

        base_frame = getattr(self.frame, _side)
        adjacent_frame_1 = getattr(self.frame, adjacent_frames[_side]["adj_1"])
        adjacent_frame_2 = getattr(self.frame, adjacent_frames[_side]["adj_2"])

        left_corner_area = base_frame.width * adjacent_frame_1.width
        right_corner_area = base_frame.width * adjacent_frame_2.width
        corner_area = ((left_corner_area) / 2) + ((right_corner_area) / 2)

        return corner_area

    def side_area(self, _side):
        # type: (str) -> float
        frame_element = getattr(self.frame, _side)
        # -- base area
        base_area = frame_element.width * self.side_interior_length(_side)
        return base_area + self.corner_area(_side)

    def side_frame_heat_loss(self, _side):
        # type: (str) -> float
        frame_element = getattr(self.frame, _side)
        return frame_element.u_factor * self.side_area(_side)

    def side_psi_glazing_heat_lost(self, _side):
        # type: (str) -> float
        frame_element = getattr(self.frame, _side)
        return frame_element.psi_glazing * self.side_interior_length(_side)

    def side_psi_install_heat_lost(self, _side):
        # type: (str) -> float
        frame_element = getattr(self.frame, _side)
        return frame_element.psi_install * self.side_exterior_length(_side)

    @property
    def heat_loss_frame(self):
        # type: () -> float
        return sum(
            [
                self.side_frame_heat_loss("top"),
                self.side_frame_heat_loss("right"),
                self.side_frame_heat_loss("bottom"),
                self.side_frame_heat_loss("left"),
            ]
        )

    @property
    def heat_loss_psi_glazing(self):
        # type: () -> float
        return sum(
            [
                self.side_psi_glazing_heat_lost("top"),
                self.side_psi_glazing_heat_lost("right"),
                self.side_psi_glazing_heat_lost("bottom"),
                self.side_psi_glazing_heat_lost("left"),
            ]
        )

    @property
    def heat_loss_psi_install(self):
        # type: () -> float
        return sum(
            [
                self.side_psi_install_heat_lost("top"),
                self.side_psi_install_heat_lost("right"),
                self.side_psi_install_heat_lost("bottom"),
                self.side_psi_install_heat_lost("left"),
            ]
        )

    @property
    def heat_loss_glazing(self):
        # type: () -> float
        return self.area_glazing * self.glazing.u_factor

    @property
    def uw(self):
        # type: () -> float
        return (
            self.heat_loss_glazing
            + self.heat_loss_frame
            + self.heat_loss_psi_glazing
            + self.heat_loss_psi_install
        ) / self.area_window


def build_standard_window(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> ISO100771Data
    """A standard-size (1.23m x 1.48m) window as per ISO 10077-2:2006, As per Annex F (2006)"""
    width = 1.23  # M
    height = 1.48  # M
    return ISO100771Data(width, height, _frame, _glazing)


def calculate_window_frame_factor(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> float
    """Calculate the frame factor for a standard-size (1.23m x 1.48m) window as per ISO 10077-2:2006, Annex-F"""
    window = build_standard_window(_frame, _glazing)
    return window.area_glazing / window.area_window


# -----------------------------------------------------------------------------
# -- Functions to calculate U-w -----------------------------------------------


def calculate_window_uw(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> float
    """Calculate U-w (W/m2k) for a standard-size (1.23m x 1.48m) window as per ISO 10077-2:2006, Annex-F
    This value includes the impact of the frame, glazing, glazing-spacers, and the psi-install heat loss.
    """

    warnings.warn(
        "The 'function calculate_window_uw' is deprecated and will be removed in a future version. Use function 'calculate_standard_window_uw' instead.",
        DeprecationWarning,
    )

    window = build_standard_window(_frame, _glazing)
    return window.uw


def calculate_standard_window_uw(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> float
    """Calculate U-w (W/m2k) for a standard-size window as per ISO 10077-2:2006
    This value includes the impact of the frame, glazing, glazing-spacers, and the psi-install heat loss.
    """

    window = build_standard_window(_frame, _glazing)
    return window.uw


def calculate_hb_aperture_uw(_hb_aperture):
    # type: (aperture.Aperture) -> float
    """Calculate U-W (W/m2k) for a 'honeybee.aperture.Aperture' with PH-Style frame and glazing as per ISO 10077-2:2006
    This value includes the impact of the frame, glazing, glazing-spacers, and the psi-install heat loss.
    """
    window = ISO100771Data.from_hb_aperture(_hb_aperture)
    return window.uw


def calculate_lbt_Face3D_uw(_hb_face3d, _ph_frame, _ph_glazing):
    # type: (face.Face3D, window.PhWindowFrame, window.PhWindowGlazing) -> float
    """Calculate U-w (W/m2k) for a 'ladybug_geometry.geometry3d.face.Face3D' as per ISO 10077-2:2006
    This value includes the impact of the frame, glazing, glazing-spacers, and the psi-install heat loss.
    """

    window = ISO100771Data.from_lbt_Face3D(_hb_face3d, _ph_frame, _ph_glazing)
    return window.uw
