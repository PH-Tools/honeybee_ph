# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Valid 'types' for PHI Certification Settings."""

from enum import Enum


class PhiCertificationType(Enum):
    PASSIVE_HOUSE = 1
    ENERPHIT = 2
    LOW_ENERGY_BUILDING = 3
    OTHER = 4


class PhiCertificationClass(Enum):
    CLASSIC = 1
    PLUS = 2
    PREMIUM = 3


class PhiCertificationPEType(Enum):
    PE = 1
    PER = 2


class PhiCertificationEnerPHitType(Enum):
    BY_COMPONENT = 1
    BY_DEMAND = 2


class PhiCertificationRetrofitType(Enum):
    NEW_BUILDING = 1
    RETROFIT = 2
    STEP_BY_STEP_RETROFIT = 3
