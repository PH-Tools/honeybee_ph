from pytest import approx
from honeybee_energy_ph.load import phius_residential

def test_cooktop():
    assert phius_residential.cooktop(3, 0.5) == approx(750.0)

def test_lighting_interior():
    assert phius_residential.lighting_interior(1000, 0.5) == approx(743.5027027027027)

def test_lighting_exterior():
    assert phius_residential.lighting_exterior(1000, 1.0) == approx(30.0)

def test_mels():
    assert phius_residential.misc_electrical(3, 1000) == approx(1224.0)

def test_lightingfgarage():
    assert phius_residential.lighting_garage(1.0) == approx(20.0)