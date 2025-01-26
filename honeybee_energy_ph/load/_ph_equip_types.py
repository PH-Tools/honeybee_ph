# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HB-PH Electric Equipment Types."""

try:
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("Failed to import honeybee_ph_utils: {}".format(e))


# -----------------------------------------------------------------------------
# - Type Enums


class PhDishwasherType(enumerables.CustomEnum):
    allowed = [
        "1-DHW CONNECTION",
        "2-COLD WATER CONNECTION",
    ]

    def __init__(self, _value=1):
        # type: (int | str) -> None
        super(PhDishwasherType, self).__init__(_value)


class PhClothesWasherType(enumerables.CustomEnum):
    allowed = [
        "1-DHW CONNECTION",
        "2-COLD WATER CONNECTION",
    ]

    def __init__(self, _value=1):
        # type: (int | str) -> None
        super(PhClothesWasherType, self).__init__(_value)


class PhClothesDryerType(enumerables.CustomEnum):
    allowed = [
        "1-CLOTHES LINE",
        "2-DRYING CLOSET (COLD!)",
        "3-DRYING CLOSET (COLD!) IN EXTRACT AIR",
        "4-CONDENSATION DRYER",
        "5-ELECTRIC EXHAUST AIR DRYER",
        "6-GAS EXHAUST AIR DRYER",
    ]

    def __init__(self, _value=1):
        # type: (int | str) -> None
        super(PhClothesDryerType, self).__init__(_value)


class PhCookingType(enumerables.CustomEnum):
    allowed = [
        "1-ELECTRICITY",
        "2-NATURAL GAS",
        "3-LPG",
    ]

    def __init__(self, _value=1):
        # type: (int | str) -> None
        super(PhCookingType, self).__init__(_value)

