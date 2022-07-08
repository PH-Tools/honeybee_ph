# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HBPH Window Objects"""

try:
    from typing import Any
except ImportError:
    pass  # Python 2.7

from honeybee_energy_ph.construction import _base


class PhWindowFrameElement(_base._Base):
    """An individual PhWindowFrameElement (side) which is part of a complete PhWindowFrame."""

    def __init__(self, _identifier):
        super(PhWindowFrameElement, self).__init__(_identifier)
        self.width = 0.1
        self.u_factor = 1.0
        self.psi_glazing = 0.04
        self.psi_install = 0.04
        self.chi_value = 0.0

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhWindowFrameElement, self).to_dict()
        d['width'] = self.width
        d['u_factor'] = self.u_factor
        d['psi_glazing'] = self.psi_glazing
        d['psi_install'] = self.psi_install
        d['chi_value'] = self.chi_value
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhWindowFrameElement
        new_obj = cls(_input_dict['identifier'])
        new_obj.set_base_attrs_from_dict(_input_dict)
        new_obj.width = _input_dict['width']
        new_obj.u_factor = _input_dict['u_factor']
        new_obj.psi_glazing = _input_dict['psi_glazing']
        new_obj.psi_install = _input_dict['psi_install']
        new_obj.chi_value = _input_dict['chi_value']
        return new_obj

    def duplicate(self):
        # type: () -> PhWindowFrameElement
        return self.__copy__()

    def __copy__(self):
        # type: () -> PhWindowFrameElement
        new_obj = self.__class__(self.identifier)
        new_obj.set_base_attrs_from_obj(self)
        new_obj.width = self.width
        new_obj.u_factor = self.u_factor
        new_obj.psi_glazing = self.psi_glazing
        new_obj.psi_install = self.psi_install
        new_obj.chi_value = self.chi_value
        return new_obj

    def __str__(self):
        return '{}(width={:.3f}, u_factor={:.3f}, psi_glazing={:.3f}, psi_install={:.3f}, chi_value={:.3f})'.format(
            self.__class__.__name__, self.width, self.u_factor, self.psi_glazing, self.psi_install, self.chi_value)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhWindowFrame(_base._Base):
    """A full PH window frame made of 4 PhWindowFrameElements."""

    def __init__(self, _identifier):
        super(PhWindowFrame, self).__init__(_identifier)
        self.top = PhWindowFrameElement('PhWindowFrameElement')
        self.right = PhWindowFrameElement('PhWindowFrameElement')
        self.bottom = PhWindowFrameElement('PhWindowFrameElement')
        self.left = PhWindowFrameElement('PhWindowFrameElement')

    @property
    def elements(self):
        return [self.top, self.right, self.bottom, self.left]

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhWindowFrame, self).to_dict()
        d['top'] = self.top.to_dict()
        d['right'] = self.right.to_dict()
        d['bottom'] = self.bottom.to_dict()
        d['left'] = self.left.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhWindowFrame
        new_obj = cls(_input_dict['identifier'])
        new_obj.set_base_attrs_from_dict(_input_dict)
        new_obj.top = PhWindowFrameElement.from_dict(_input_dict['top'])
        new_obj.right = PhWindowFrameElement.from_dict(_input_dict['right'])
        new_obj.bottom = PhWindowFrameElement.from_dict(_input_dict['bottom'])
        new_obj.left = PhWindowFrameElement.from_dict(_input_dict['left'])
        return new_obj

    def duplicate(self):
        # type: () -> PhWindowFrame
        return self.__copy__()

    def __copy__(self):
        # type: () -> PhWindowFrame
        new_obj = self.__class__(self.identifier)
        new_obj.set_base_attrs_from_obj(self)
        new_obj.top = self.top.duplicate()
        new_obj.right = self.right.duplicate()
        new_obj.bottom = self.bottom.duplicate()
        new_obj.left = self.left.duplicate()
        return new_obj

    def __str__(self):
        return '{}(top={!r}, right={!r}, bottom={!r}, left={!r})'.format(
            self.__class__.__name__, self.top, self.right, self.bottom, self.left)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhWindowGlazing(_base._Base):
    def __init__(self, _identifier):
        super(PhWindowGlazing, self).__init__(_identifier)
        self.u_factor = 1.0
        self.g_value = 0.4

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhWindowGlazing, self).to_dict()
        d['u_factor'] = self.u_factor
        d['g_value'] = self.g_value
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhWindowGlazing
        new_obj = cls(_input_dict['identifier'])
        new_obj.set_base_attrs_from_dict(_input_dict)
        new_obj.u_factor = _input_dict['u_factor']
        new_obj.g_value = _input_dict['g_value']
        return new_obj

    def duplicate(self):
        # type: () -> PhWindowGlazing
        return self.__copy__()

    def __copy__(self):
        # type: () -> PhWindowGlazing
        new_obj = self.__class__(self.identifier)
        new_obj.set_base_attrs_from_obj(self)
        new_obj.u_factor = self.u_factor
        new_obj.g_value = self.g_value
        return new_obj

    def __str__(self):
        return '{}(u_factor={:.3f}, g_value={:.3f})'.format(
            self.__class__.__name__, self.u_factor, self.g_value)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
