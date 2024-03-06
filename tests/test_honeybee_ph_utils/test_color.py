from honeybee_ph_utils.color import PhColor

class MockSystemColor(object):
    """Protocol for System.Drawing.Color from .NET"""
    def __init__(self, a, r, g, b):
        self.A = a
        self.R = r
        self.G = g
        self.B = b

def test_ph_color_values_over_255():
    color = PhColor.from_argb(300, 300, 300, 300)
    assert color.a == 255
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255

def test_ph_color_values_under_0():
    color = PhColor.from_argb(-10, -10, -10, -10)
    assert color.a == 0
    assert color.r == 0
    assert color.g == 0
    assert color.b == 0

def test_ph_color_from_argb():
    color = PhColor.from_argb(255, 255, 255, 255)
    assert color.a == 255
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255

def test_ph_color_from_rgb():
    color = PhColor.from_rgb(255, 255, 255)
    assert color.a == 255
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255

def test_ph_color_from_system_color():
    color = PhColor.from_system_color(
        MockSystemColor(255, 255, 255, 255)
    )
    assert color.a == 255
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255

def test_ph_color_to_dict():
    color = PhColor.from_argb(255, 255, 255, 255)
    assert color.to_dict() == {'a': 255, 'r': 255, 'g': 255, 'b': 255}

def test_ph_color_from_dict():
    color = PhColor.from_dict({'a': 255, 'r': 255, 'g': 255, 'b': 255})
    assert color is not None
    assert color.a == 255
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255

def test_ph_color_str():
    color = PhColor.from_argb(255, 255, 255, 255)
    assert str(color) == 'Color(a=255, r=255, g=255, b=255)'
    assert repr(color) == 'Color(a=255, r=255, g=255, b=255)'

def test_ph_color_from_dict_none():
    color = PhColor.from_dict(None)
    assert color == None

def test_ph_color_from_dict_empty():
    color = PhColor.from_dict({})
    assert color == None

def test_copy_color():
    color = PhColor.from_argb(255, 255, 255, 255)
    color2 = color.duplicate()
    assert color2.a == 255
    assert color2.r == 255
    assert color2.g == 255
    assert color2.b == 255
    assert color2 == color
    assert color2 is not color
    color2.a = 0
    assert color2.a == 0
    assert color.a == 255
    assert color2 != color

