# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""TextAnnotations class used for writing to PDF."""

try:
    from typing import Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from System.Drawing import Color
except ImportError:
    pass  # Outside .NET

try:
    from Rhino.Geometry import TextJustification, Point3d
    from Rhino.DocObjects.DimensionStyle import MaskFrame
except ImportError:
    pass  # Outside Rhino

from honeybee_ph_rhino.gh_compo_io import ghio_validators


class RHTextJustify(ghio_validators.Validated):
    """Validator for Integer user-input conversion into Rhino.Geometry.TextJustification Enum."""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        if isinstance(new_value, TextJustification):
            return new_value

        # if it's an integer input, convert to a TextJustification
        mapping = {
            0: TextJustification.BottomLeft, 1: TextJustification.BottomCenter,
            2: TextJustification.BottomRight, 3: TextJustification.MiddleLeft,
            4: TextJustification.MiddleCenter, 5: TextJustification.MiddleRight,
            6: TextJustification.TopLeft, 7: TextJustification.TopCenter,
            8: TextJustification.TopRight
        }

        try:
            return mapping[int(new_value)]
        except KeyError as e:
            msg = "Error: Key {} is not a valid Text Justification?".format(new_value)
            raise KeyError("{}\n{}".format(e, msg))


class TextAnnotation(object):
    """Dataclass for Layout-Page Labels."""
    justification = RHTextJustify('justification')

    def __init__(self, _text, _size, _location, _format="{}", _justification=3,
                 _mask_draw=False, _mask_color=None, _mask_offset=0.02,
                 _mask_frame=None, _mask_draw_frame=False):
        # type: (str, float, Point3d, str, int, bool, Optional[Color], float, Optional[MaskFrame], bool) -> None
        self._text = _text
        self.text_size = _size
        self.location = _location
        self.format = _format
        self.justification = _justification
        self.mask_draw = _mask_draw
        self.mask_color = _mask_color or Color.FromArgb(50, 0, 0, 0)
        self.mask_offset = _mask_offset
        self.mask_frame = _mask_frame or MaskFrame.RectFrame
        self.mask_draw_frame = _mask_draw_frame

    @property
    def text(self):
        fmt = "{}".format(self.format)
        try:
            return fmt.format(self._text)
        except ValueError:
            try:
                return fmt.format(float(self._text))
            except Exception:
                return self._text

    def duplicate(self):
        # type: () -> TextAnnotation
        return self.__copy__()

    def __copy__(self):
        # type: () -> TextAnnotation
        return TextAnnotation(
            self._text,
            self.text_size,
            self.location,
            self.format,
            self.justification,
            self.mask_draw,
            self.mask_color,
            self.mask_offset,
            self.mask_frame,
            self.mask_draw_frame,
        )

    def _truncate(self, txt):
        # type: (str) -> str
        limit = 20
        if len(txt) > limit:
            return "{}...".format(txt.replace("\n", "")[:limit])
        else:
            return txt

    def __str__(self):
        return '{}(text={}, text_size={}, location={}, format={}, justification={})'.format(
            self.__class__.__name__, self._truncate(self.text), self.text_size, self.location, self._truncate(self.format), self.justification)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
