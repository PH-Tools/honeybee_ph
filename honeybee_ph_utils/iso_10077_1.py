# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Calculate Window U-w as per ISO-10077-2:2006"""

from honeybee_energy_ph.construction import window


class StandardWindow:
    """Temporary class to bundle calculation behavior for a standard side window."""

    def __init__(self, _win_width, _win_height, _frame, _glazing):
        self.win_width = _win_width
        self.win_height = _win_height
        self.frame = _frame
        self.glazing = _glazing

    @property
    def area_window(self):
        # type: () -> float
        return self.side_exterior_length('right') * self.side_exterior_length('top')

    @property
    def area_glazing(self):
        # type: () -> float
        return self.side_interior_length('right') * self.side_interior_length('top')

    def side_interior_length(self, _side):
        # type: (str) -> float
        side_lengths = {
            'top': (self.win_width - self.frame.right.width - self.frame.left.width),
            'right': (self.win_height - self.frame.top.width - self.frame.bottom.width),
            'bottom': (self.win_width - self.frame.right.width - self.frame.left.width),
            'left': (self.win_height - self.frame.top.width - self.frame.bottom.width),
        }
        return side_lengths[_side]

    def side_exterior_length(self, _side):
        # type: (str) -> float
        side_lengths = {
            'top': self.win_width,
            'right': self.win_height,
            'bottom': self.win_width,
            'left': self.win_height,
        }
        return side_lengths[_side]

    def corner_area(self, _side):
        # type: (str) -> float
        """Correct for the overlap / 45 degrees at the corners"""

        adjacent_frames = {
            'top': {'adj_1': 'left', 'adj_2': 'right'},
            'right': {'adj_1': 'top', 'adj_2': 'bottom'},
            'bottom': {'adj_1': 'left', 'adj_2': 'right'},
            'left': {'adj_1': 'top', 'adj_2': 'bottom'},
        }

        base_frame = getattr(self.frame, _side)
        adjacent_frame_1 = getattr(self.frame, adjacent_frames[_side]['adj_1'])
        adjacent_frame_2 = getattr(self.frame, adjacent_frames[_side]['adj_2'])

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


def build_standard_window(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> StandardWindow
    # As per Annex F (2006)
    width = 1.23  # M
    height = 1.48  # M
    return StandardWindow(width, height, _frame, _glazing)


def calculate_window_frame_factor(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> float
    window = build_standard_window(_frame, _glazing)
    return window.area_glazing / window.area_window


def calculate_window_uw(_frame, _glazing):
    # type: (window.PhWindowFrame, window.PhWindowGlazing) -> float
    window = build_standard_window(_frame, _glazing)

    heat_loss_frame = sum([
        window.side_frame_heat_loss('top'),
        window.side_frame_heat_loss('right'),
        window.side_frame_heat_loss('bottom'),
        window.side_frame_heat_loss('left')
    ])

    heat_loss_psi_glazing = sum([
        window.side_psi_glazing_heat_lost('top'),
        window.side_psi_glazing_heat_lost('right'),
        window.side_psi_glazing_heat_lost('bottom'),
        window.side_psi_glazing_heat_lost('left')
    ])

    heat_loss_psi_install = sum([
        window.side_psi_install_heat_lost('top'),
        window.side_psi_install_heat_lost('right'),
        window.side_psi_install_heat_lost('bottom'),
        window.side_psi_install_heat_lost('left')
    ])
    heat_loss_glazing = window.area_glazing * window.glazing.u_factor

    uw = (heat_loss_glazing + heat_loss_frame +
          heat_loss_psi_glazing + heat_loss_psi_install) / window.area_window

    return uw
