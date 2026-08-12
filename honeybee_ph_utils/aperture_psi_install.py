# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Resolve the effective per-edge Psi-Install values for a honeybee Aperture.

This module is the single source of truth for combining the aperture-level
'Install Type' assignments (AperturePhProperties.install_types) with the
construction-level frame-element defaults (PhWindowFrameElement.psi_install).
Every consumer of effective psi-install values (ISO 10077-1 U-w calculation,
PHX conversion, reports) should resolve them through this module.

Resolution, per side (top / right / bottom / left):
    1. If the aperture has a PhApertureInstallType assigned for the side, use
       that Install Type's psi_install value.
    2. Otherwise inherit the psi_install of the window construction's
       PhWindowFrameElement for that side.
There are no other hidden defaults.
"""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee.aperture import Aperture
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))

try:
    from honeybee_energy_ph.construction.window import PhWindowFrame, PhWindowGlazing
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph:\n\t{}".format(e))


def _get_window_construction_ph_properties(_hb_aperture):
    # type: (Aperture) -> Optional[Any]
    """Return the PH properties of the Aperture's window construction, or None.

    Handles both a plain WindowConstruction and a WindowConstructionShade
    (which wraps the real WindowConstruction in its 'window_construction' attribute).
    """
    construction = _hb_aperture.properties.energy.construction  # type: ignore
    construction = getattr(construction, "window_construction", construction)
    return getattr(construction.properties, "ph", None)


def get_ph_frame(_hb_aperture):
    # type: (Aperture) -> Optional[PhWindowFrame]
    """Return the PH frame of the Aperture's window construction, or None."""
    return getattr(_get_window_construction_ph_properties(_hb_aperture), "ph_frame", None)


def get_ph_glazing(_hb_aperture):
    # type: (Aperture) -> Optional[PhWindowGlazing]
    """Return the PH glazing of the Aperture's window construction, or None."""
    return getattr(_get_window_construction_ph_properties(_hb_aperture), "ph_glazing", None)


def _resolve_side_psi_install(_side, _install_types, _ph_frame, _aperture_display_name):
    # type: (str, Any, Optional[PhWindowFrame], str) -> float
    """Return the effective psi-install (W/mK) for one side.

    The single resolution rule: the side's assigned Install Type if there is one,
    otherwise the construction frame element's psi_install.
    """
    install_type = _install_types.get_side(_side)
    if install_type is not None:
        return install_type.psi_install
    if _ph_frame is not None:
        return getattr(_ph_frame, _side).psi_install
    raise ValueError(
        "Cannot resolve the '{}' psi-install for Aperture '{}': no Install Type "
        "is assigned and the window construction has no PH frame to inherit from.".format(_side, _aperture_display_name)
    )


def resolve_psi_install_values(_hb_aperture):
    # type: (Aperture) -> Dict[str, float]
    """Return the effective psi-install value (W/mK) for each side of an Aperture.

    Keys are 'top' / 'right' / 'bottom' / 'left' (PhWindowFrame element order).
    Raises ValueError if a side has no Install Type assigned and the window
    construction has no PH frame to inherit from.
    """
    install_types = _hb_aperture.properties.ph.install_types  # type: ignore
    ph_frame = get_ph_frame(_hb_aperture)
    return {
        side: _resolve_side_psi_install(side, install_types, ph_frame, _hb_aperture.display_name)
        for side in install_types.SIDES
    }


def resolve_effective_frame(_hb_aperture):
    # type: (Aperture) -> PhWindowFrame
    """Return a transient duplicate of the Aperture's PH frame with resolved psi-install values.

    The duplicate has each side's psi_install overridden by the aperture's assigned
    Install Type (where one is assigned). Nothing new is serialized: the result is an
    in-memory frame for calculations (eg. ISO 10077-1 U-w) only.
    Raises ValueError if the window construction has no PH frame.
    """
    ph_frame = get_ph_frame(_hb_aperture)
    if ph_frame is None:
        raise ValueError(
            "Cannot build an effective frame for Aperture '{}': the window construction "
            "has no PH frame.".format(_hb_aperture.display_name)
        )

    effective_frame = ph_frame.duplicate()
    install_types = _hb_aperture.properties.ph.install_types  # type: ignore
    for side in install_types.SIDES:
        getattr(effective_frame, side).psi_install = _resolve_side_psi_install(
            side, install_types, ph_frame, _hb_aperture.display_name
        )
    return effective_frame
