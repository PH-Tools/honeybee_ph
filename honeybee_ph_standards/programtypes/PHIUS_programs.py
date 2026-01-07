# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Phius Program Data Library"""

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7


# Programs from:
# - PHIUS Guidebook, Table N-10, v3.02 | July 2021
# - Honeybee ASHRAE 90.1 2019 | IECC 2021
PHIUS_Non_Res = {
    "2021::PHIUS_NR::Assembly": {
        "name": "Assembly",
        "hb_base_program": "2019::Courthouse::Courtroom",
        "protocol": "PHIUS_NonRes",
        "description": "Fair/Congress building",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::Courthouse::Courtroom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Assembly",
                "identifier": "2021::PHIUS_NR::Assembly",
                "start_hour": 13,
                "end_hour": 18,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Assembly",
                "name": "2021::PHIUS_NR::Assembly",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Assembly",
                "name": "2021::PHIUS_NR::Assembly",
                "daily_operating_hours": 5,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Assembly",
                "name": "2021::PHIUS_NR::Assembly",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 12.91668,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Assembly",
                "name": "2021::PHIUS_NR::Assembly",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Assembly",
                "name": "2021::PHIUS_NR::Assembly",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Theater_Ticketing": {
        "name": "Theater Ticketing",
        "hb_base_program": "2019::Retail::Entry",
        "protocol": "PHIUS_NonRes",
        "description": "Booking hall",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Entry"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Theater_Ticketing",
                "identifier": "2021::PHIUS_NR::Theater_Ticketing",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Ticketing",
                "name": "2021::PHIUS_NR::Theater_Ticketing",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Ticketing",
                "name": "2021::PHIUS_NR::Theater_Ticketing",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Ticketing",
                "name": "2021::PHIUS_NR::Theater_Ticketing",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 9.041676,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Ticketing",
                "name": "2021::PHIUS_NR::Theater_Ticketing",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Ticketing",
                "name": "2021::PHIUS_NR::Theater_Ticketing",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Canteen": {
        "name": "Canteen",
        "hb_base_program": "2019::QuickServiceRestaurant::Dining",
        "protocol": "PHIUS_NonRes",
        "description": "2021::PHIUS_NR::Canteen",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::QuickServiceRestaurant::Dining",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Canteen",
                "identifier": "2021::PHIUS_NR::Canteen",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Canteen",
                "name": "2021::PHIUS_NR::Canteen",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Canteen",
                "name": "2021::PHIUS_NR::Canteen",
                "daily_operating_hours": 7,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Canteen",
                "name": "2021::PHIUS_NR::Canteen",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.45834,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Canteen",
                "name": "2021::PHIUS_NR::Canteen",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Canteen",
                "name": "2021::PHIUS_NR::Canteen",
                "watts_per_m2": 116.788315,
            },
        },
    },
    "2021::PHIUS_NR::Hallway": {
        "name": "Hallway",
        "hb_base_program": "2019::MidriseApartment::Corridor",
        "protocol": "PHIUS_NonRes",
        "description": "Traffic / Circulation Areas",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::MidriseApartment::Corridor",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Hallway",
                "identifier": "2021::PHIUS_NR::Hallway",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.2,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hallway",
                "name": "2021::PHIUS_NR::Hallway",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Hallway",
                "name": "2021::PHIUS_NR::Hallway",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hallway",
                "name": "2021::PHIUS_NR::Hallway",
                "target_lux": 100,
                "target_lux_height": 0.0,
                "watts_per_m2": 5.381955,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Hallway",
                "name": "2021::PHIUS_NR::Hallway",
                "annual_utilization_factor": 0.245833,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hallway",
                "name": "2021::PHIUS_NR::Hallway",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Classroom": {
        "name": "Classroom",
        "hb_base_program": "2019::PrimarySchool::Classroom",
        "protocol": "PHIUS_NonRes",
        "description": "Classroom (school and nursery school)",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::PrimarySchool::Classroom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Classroom",
                "identifier": "2021::PHIUS_NR::Classroom",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Classroom",
                "name": "2021::PHIUS_NR::Classroom",
                "people_per_area": 0.269098,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Classroom",
                "name": "2021::PHIUS_NR::Classroom",
                "daily_operating_hours": 7,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.9,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Classroom",
                "name": "2021::PHIUS_NR::Classroom",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 7.642369,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Classroom",
                "name": "2021::PHIUS_NR::Classroom",
                "annual_utilization_factor": 0.442427,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Classroom",
                "name": "2021::PHIUS_NR::Classroom",
                "watts_per_m2": 14.999495,
            },
        },
    },
    "2021::PHIUS_NR::Garage_Private": {
        "name": "Garage Private",
        "hb_base_program": "2019::Courthouse::Parking",
        "protocol": "PHIUS_NonRes",
        "description": "Garage buildings for offices and private use",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::Courthouse::Parking",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Garage_Private",
                "identifier": "2021::PHIUS_NR::Garage_Private",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.05,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Garage_Private",
                "name": "2021::PHIUS_NR::Garage_Private",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Garage_Private",
                "name": "2021::PHIUS_NR::Garage_Private",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Garage_Private",
                "name": "2021::PHIUS_NR::Garage_Private",
                "target_lux": 75,
                "target_lux_height": 0.0,
                "watts_per_m2": 1.614585,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Garage_Private",
                "name": "2021::PHIUS_NR::Garage_Private",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Garage_Private",
                "name": "2021::PHIUS_NR::Garage_Private",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Garage_Public": {
        "name": "Garage Public",
        "hb_base_program": "2019::Courthouse::Parking",
        "protocol": "PHIUS_NonRes",
        "description": "Garage buildings for public use",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::Courthouse::Parking",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Garage_Public",
                "identifier": "2021::PHIUS_NR::Garage_Public",
                "start_hour": 9,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.2,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Garage_Public",
                "name": "2021::PHIUS_NR::Garage_Public",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Garage_Public",
                "name": "2021::PHIUS_NR::Garage_Public",
                "daily_operating_hours": 15,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Garage_Public",
                "name": "2021::PHIUS_NR::Garage_Public",
                "target_lux": 100,
                "target_lux_height": 0.0,
                "watts_per_m2": 1.614585,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Garage_Public",
                "name": "2021::PHIUS_NR::Garage_Public",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Garage_Public",
                "name": "2021::PHIUS_NR::Garage_Public",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Gym": {
        "name": "Gym",
        "hb_base_program": "2019::SmallHotel::Exercise",
        "protocol": "PHIUS_NonRes",
        "description": "Sports hall (without public viewing area)",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::SmallHotel::Exercise",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Gym",
                "identifier": "2021::PHIUS_NR::Gym",
                "start_hour": 8,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Gym",
                "name": "2021::PHIUS_NR::Gym",
                "people_per_area": 0.214632,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Gym",
                "name": "2021::PHIUS_NR::Gym",
                "daily_operating_hours": 15,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Gym",
                "name": "2021::PHIUS_NR::Gym",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 9.68751,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Gym",
                "name": "2021::PHIUS_NR::Gym",
                "annual_utilization_factor": 0.4375,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Gym",
                "name": "2021::PHIUS_NR::Gym",
                "watts_per_m2": 18.621547,
            },
        },
    },
    "2021::PHIUS_NR::Hospital_Ward": {
        "name": "Hospital Ward",
        "hb_base_program": "2019::Hospital::PatRoom",
        "protocol": "PHIUS_NonRes",
        "description": "Hospital ward or dormitory",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Hospital::PatRoom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Hospital_Ward",
                "identifier": "2021::PHIUS_NR::Hospital_Ward",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hospital_Ward",
                "name": "2021::PHIUS_NR::Hospital_Ward",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Hospital_Ward",
                "name": "2021::PHIUS_NR::Hospital_Ward",
                "daily_operating_hours": 7,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hospital_Ward",
                "name": "2021::PHIUS_NR::Hospital_Ward",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 7.319452,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Hospital_Ward",
                "name": "2021::PHIUS_NR::Hospital_Ward",
                "annual_utilization_factor": 0.594292,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hospital_Ward",
                "name": "2021::PHIUS_NR::Hospital_Ward",
                "watts_per_m2": 21.5278,
            },
        },
    },
    "2021::PHIUS_NR::Hotel_Bedroom": {
        "name": "Hotel Bedroom",
        "hb_base_program": "2019::LargeHotel::GuestRoom",
        "protocol": "PHIUS_NonRes",
        "description": "Hotel bedroom",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::LargeHotel::GuestRoom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Hotel_Bedroom",
                "identifier": "2021::PHIUS_NR::Hotel_Bedroom",
                "start_hour": 21,
                "end_hour": 8,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.25,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hotel_Bedroom",
                "name": "2021::PHIUS_NR::Hotel_Bedroom",
                "people_per_area": 0.038427,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Hotel_Bedroom",
                "name": "2021::PHIUS_NR::Hotel_Bedroom",
                "daily_operating_hours": 11,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.3,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hotel_Bedroom",
                "name": "2021::PHIUS_NR::Hotel_Bedroom",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 4.413199,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Hotel_Bedroom",
                "name": "2021::PHIUS_NR::Hotel_Bedroom",
                "annual_utilization_factor": 0.315303,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Hotel_Bedroom",
                "name": "2021::PHIUS_NR::Hotel_Bedroom",
                "watts_per_m2": 6.748965,
            },
        },
    },
    "2021::PHIUS_NR::Kitchen_Commercial_Cooking": {
        "name": "Kitchen Commercial Cooking",
        "hb_base_program": "2019::FullServiceRestaurant::Kitchen",
        "protocol": "PHIUS_NonRes",
        "description": "Kitchen in non-residential buildings",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::FullServiceRestaurant::Kitchen",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "start_hour": 10,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "daily_operating_hours": 13,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 11.732651,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Cooking",
                "watts_per_m2": 403.969167,
            },
        },
    },
    "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room": {
        "name": "Kitchen Commercial Prep Room",
        "hb_base_program": "2019::SuperMarket::Deli",
        "protocol": "PHIUS_NonRes",
        "description": "Kitchen preparation room or storeroom",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SuperMarket::Deli"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "start_hour": 7,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "people_per_area": 0.086111,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "daily_operating_hours": 16,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 11.732651,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "annual_utilization_factor": 0.606735,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS_NR::Kitchen_Commercial_Prep_Room",
                "watts_per_m2": 8.934037,
            },
        },
    },
    "2021::PHIUS_NR::Laundry_Public": {
        "name": "Laundry Public",
        "hb_base_program": "2019::LargeHotel::Laundry",
        "protocol": "PHIUS_NonRes",
        "description": "Common Laundry",
        "source": ["MF_Calculator_2021", "2019::LargeHotel::Laundry"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Laundry_Public",
                "identifier": "2021::PHIUS_NR::Laundry_Public",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Laundry_Public",
                "name": "2021::PHIUS_NR::Laundry_Public",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Laundry_Public",
                "name": "2021::PHIUS_NR::Laundry_Public",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Laundry_Public",
                "name": "2021::PHIUS_NR::Laundry_Public",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 5.704867,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Laundry_Public",
                "name": "2021::PHIUS_NR::Laundry_Public",
                "annual_utilization_factor": 0.447888,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Laundry_Public",
                "name": "2021::PHIUS_NR::Laundry_Public",
                "watts_per_m2": 61.677147,
            },
        },
    },
    "2021::PHIUS_NR::Library_Reading_Room": {
        "name": "Library Reading Room",
        "hb_base_program": "2019::SecondarySchool::Library",
        "protocol": "PHIUS_NonRes",
        "description": "Library - reading rooms",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::SecondarySchool::Library",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Library_Reading_Room",
                "identifier": "2021::PHIUS_NR::Library_Reading_Room",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Reading_Room",
                "name": "2021::PHIUS_NR::Library_Reading_Room",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Library_Reading_Room",
                "name": "2021::PHIUS_NR::Library_Reading_Room",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Reading_Room",
                "name": "2021::PHIUS_NR::Library_Reading_Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Library_Reading_Room",
                "name": "2021::PHIUS_NR::Library_Reading_Room",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Reading_Room",
                "name": "2021::PHIUS_NR::Library_Reading_Room",
                "watts_per_m2": 10.010427,
            },
        },
    },
    "2021::PHIUS_NR::Library_Storage": {
        "name": "Library Storage",
        "hb_base_program": "2019::SecondarySchool::Library",
        "protocol": "PHIUS_NonRes",
        "description": "Library magazine and stores",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Library_Storage",
                "identifier": "2021::PHIUS_NR::Library_Storage",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Storage",
                "name": "2021::PHIUS_NR::Library_Storage",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Library_Storage",
                "name": "2021::PHIUS_NR::Library_Storage",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Storage",
                "name": "2021::PHIUS_NR::Library_Storage",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Library_Storage",
                "name": "2021::PHIUS_NR::Library_Storage",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Storage",
                "name": "2021::PHIUS_NR::Library_Storage",
                "watts_per_m2": 10.010427,
            },
        },
    },
    "2021::PHIUS_NR::Library_Stacks": {
        "name": "Library Stacks",
        "hb_base_program": "2019::SecondarySchool::Library",
        "protocol": "PHIUS_NonRes",
        "description": "Library-open stacks areas",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Library_Stacks",
                "identifier": "2021::PHIUS_NR::Library_Stacks",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Stacks",
                "name": "2021::PHIUS_NR::Library_Stacks",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Library_Stacks",
                "name": "2021::PHIUS_NR::Library_Stacks",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Stacks",
                "name": "2021::PHIUS_NR::Library_Stacks",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Library_Stacks",
                "name": "2021::PHIUS_NR::Library_Stacks",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Library_Stacks",
                "name": "2021::PHIUS_NR::Library_Stacks",
                "watts_per_m2": 10.010427,
            },
        },
    },
    "2021::PHIUS_NR::Museum_Exhibition": {
        "name": "Museum Exhibition",
        "hb_base_program": "2019::Retail::Retail",
        "protocol": "PHIUS_NonRes",
        "description": "Exhibition rooms and museums with conservation requirements",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Retail"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Museum_Exhibition",
                "identifier": "2021::PHIUS_NR::Museum_Exhibition",
                "start_hour": 10,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Museum_Exhibition",
                "name": "2021::PHIUS_NR::Museum_Exhibition",
                "people_per_area": 0.161459,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Museum_Exhibition",
                "name": "2021::PHIUS_NR::Museum_Exhibition",
                "daily_operating_hours": 8,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Museum_Exhibition",
                "name": "2021::PHIUS_NR::Museum_Exhibition",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Museum_Exhibition",
                "name": "2021::PHIUS_NR::Museum_Exhibition",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Museum_Exhibition",
                "name": "2021::PHIUS_NR::Museum_Exhibition",
                "watts_per_m2": 3.22917,
            },
        },
    },
    "2021::PHIUS_NR::Server_Room": {
        "name": "Server Room",
        "hb_base_program": "2019::MediumOffice::Elec/MechRoom",
        "protocol": "PHIUS_NonRes",
        "description": "Server room, computer center",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::MediumOffice::Elec/MechRoom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Server_Room",
                "identifier": "2021::PHIUS_NR::Server_Room",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Server_Room",
                "name": "2021::PHIUS_NR::Server_Room",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Server_Room",
                "name": "2021::PHIUS_NR::Server_Room",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Server_Room",
                "name": "2021::PHIUS_NR::Server_Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 4.628477,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Server_Room",
                "name": "2021::PHIUS_NR::Server_Room",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Server_Room",
                "name": "2021::PHIUS_NR::Server_Room",
                "watts_per_m2": 2.906253,
            },
        },
    },
    "2021::PHIUS_NR::Manufacturing_Workshop": {
        "name": "Manufacturing Workshop",
        "hb_base_program": "2019::Laboratory::Open lab",
        "protocol": "PHIUS_NonRes",
        "description": "Workshop, assembly,manufacturing",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::Laboratory::Open lab",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Manufacturing_Workshop",
                "identifier": "2021::PHIUS_NR::Manufacturing_Workshop",
                "start_hour": 7,
                "end_hour": 16,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Manufacturing_Workshop",
                "name": "2021::PHIUS_NR::Manufacturing_Workshop",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Manufacturing_Workshop",
                "name": "2021::PHIUS_NR::Manufacturing_Workshop",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Manufacturing_Workshop",
                "name": "2021::PHIUS_NR::Manufacturing_Workshop",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 14.315987,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Manufacturing_Workshop",
                "name": "2021::PHIUS_NR::Manufacturing_Workshop",
                "annual_utilization_factor": 0.307021,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Manufacturing_Workshop",
                "name": "2021::PHIUS_NR::Manufacturing_Workshop",
                "watts_per_m2": 43.0556,
            },
        },
    },
    "2021::PHIUS_NR::Office_Meeting_Room": {
        "name": "Office Meeting Room",
        "hb_base_program": "2019::LargeOffice::Conference",
        "protocol": "PHIUS_NonRes",
        "description": "Meeting conference and seminar room",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::LargeOffice::Conference",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Office_Meeting_Room",
                "identifier": "2021::PHIUS_NR::Office_Meeting_Room",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Meeting_Room",
                "name": "2021::PHIUS_NR::Office_Meeting_Room",
                "people_per_area": 0.538196,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Meeting_Room",
                "name": "2021::PHIUS_NR::Office_Meeting_Room",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Meeting_Room",
                "name": "2021::PHIUS_NR::Office_Meeting_Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 10.440983,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Meeting_Room",
                "name": "2021::PHIUS_NR::Office_Meeting_Room",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Meeting_Room",
                "name": "2021::PHIUS_NR::Office_Meeting_Room",
                "watts_per_m2": 3.982643,
            },
        },
    },
    "2021::PHIUS_NR::Office_Workspace_Open": {
        "name": "Office Workspace Open",
        "hb_base_program": "2019::LargeOffice::OpenOffice",
        "protocol": "PHIUS_NonRes",
        "description": "Landscaped office (seven or more workplaces)",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::LargeOffice::OpenOffice",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Office_Workspace_Open",
                "identifier": "2021::PHIUS_NR::Office_Workspace_Open",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Open",
                "name": "2021::PHIUS_NR::Office_Workspace_Open",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Open",
                "name": "2021::PHIUS_NR::Office_Workspace_Open",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Open",
                "name": "2021::PHIUS_NR::Office_Workspace_Open",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Open",
                "name": "2021::PHIUS_NR::Office_Workspace_Open",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Open",
                "name": "2021::PHIUS_NR::Office_Workspace_Open",
                "watts_per_m2": 7.642369,
            },
        },
    },
    "2021::PHIUS_NR::Office_Workspace_Semiopen": {
        "name": "Office Workspace Semiopen",
        "hb_base_program": "2019::LargeOffice::ClosedOffice",
        "protocol": "PHIUS_NonRes",
        "description": "Workgroup Office (2-6 workplaces)",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::LargeOffice::ClosedOffice",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "identifier": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "name": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "people_per_area": 0.051129,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "name": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "name": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 7.965286,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "name": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "name": "2021::PHIUS_NR::Office_Workspace_Semiopen",
                "watts_per_m2": 6.888896,
            },
        },
    },
    "2021::PHIUS_NR::Office_Workspace_Closed": {
        "name": "Office Workspace Closed",
        "hb_base_program": "2019::MediumOffice::ClosedOffice",
        "protocol": "PHIUS_NonRes",
        "description": "Personal office (single occupant)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Office_Workspace_Closed",
                "identifier": "2021::PHIUS_NR::Office_Workspace_Closed",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Closed",
                "name": "2021::PHIUS_NR::Office_Workspace_Closed",
                "people_per_area": 0.051129,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Closed",
                "name": "2021::PHIUS_NR::Office_Workspace_Closed",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Closed",
                "name": "2021::PHIUS_NR::Office_Workspace_Closed",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 7.965286,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Closed",
                "name": "2021::PHIUS_NR::Office_Workspace_Closed",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Office_Workspace_Closed",
                "name": "2021::PHIUS_NR::Office_Workspace_Closed",
                "watts_per_m2": 6.888896,
            },
        },
    },
    "2021::PHIUS_NR::Other_Habitable": {
        "name": "Other Habitable",
        "hb_base_program": "2019::LargeOffice::OpenOffice",
        "protocol": "PHIUS_NonRes",
        "description": "Other Habitable Room",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::LargeOffice::OpenOffice",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Other_Habitable",
                "identifier": "2021::PHIUS_NR::Other_Habitable",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Other_Habitable",
                "name": "2021::PHIUS_NR::Other_Habitable",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Other_Habitable",
                "name": "2021::PHIUS_NR::Other_Habitable",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Other_Habitable",
                "name": "2021::PHIUS_NR::Other_Habitable",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Other_Habitable",
                "name": "2021::PHIUS_NR::Other_Habitable",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Other_Habitable",
                "name": "2021::PHIUS_NR::Other_Habitable",
                "watts_per_m2": 7.642369,
            },
        },
    },
    "2021::PHIUS_NR::Other_Non_Habitable": {
        "name": "Other Non Habitable",
        "hb_base_program": "2019::LargeOffice::Storage",
        "protocol": "PHIUS_NonRes",
        "description": "Auxiliary spaces without habitable rooms",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::LargeOffice::Storage",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Other_Non_Habitable",
                "identifier": "2021::PHIUS_NR::Other_Non_Habitable",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Other_Non_Habitable",
                "name": "2021::PHIUS_NR::Other_Non_Habitable",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Other_Non_Habitable",
                "name": "2021::PHIUS_NR::Other_Non_Habitable",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Other_Non_Habitable",
                "name": "2021::PHIUS_NR::Other_Non_Habitable",
                "target_lux": 100,
                "target_lux_height": 0.8,
                "watts_per_m2": 4.090282,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Other_Non_Habitable",
                "name": "2021::PHIUS_NR::Other_Non_Habitable",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Other_Non_Habitable",
                "name": "2021::PHIUS_NR::Other_Non_Habitable",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Restaurant": {
        "name": "Restaurant",
        "hb_base_program": "2019::FullServiceRestaurant::Dining",
        "protocol": "PHIUS_NonRes",
        "description": "2021::PHIUS_NR::Restaurant",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::FullServiceRestaurant::Dining",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Restaurant",
                "identifier": "2021::PHIUS_NR::Restaurant",
                "start_hour": 10,
                "end_hour": 24,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Restaurant",
                "name": "2021::PHIUS_NR::Restaurant",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Restaurant",
                "name": "2021::PHIUS_NR::Restaurant",
                "daily_operating_hours": 14,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Restaurant",
                "name": "2021::PHIUS_NR::Restaurant",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.45834,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Restaurant",
                "name": "2021::PHIUS_NR::Restaurant",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Restaurant",
                "name": "2021::PHIUS_NR::Restaurant",
                "watts_per_m2": 64.927845,
            },
        },
    },
    "2021::PHIUS_NR::Restroom_Public": {
        "name": "Restroom Public",
        "hb_base_program": "2019::MediumOffice::Restroom",
        "protocol": "PHIUS_NonRes",
        "description": "Toilets and sanitary facilities in non residential buildings",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::MediumOffice::Restroom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Restroom_Public",
                "identifier": "2021::PHIUS_NR::Restroom_Public",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Restroom_Public",
                "name": "2021::PHIUS_NR::Restroom_Public",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Restroom_Public",
                "name": "2021::PHIUS_NR::Restroom_Public",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Restroom_Public",
                "name": "2021::PHIUS_NR::Restroom_Public",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.781257,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Restroom_Public",
                "name": "2021::PHIUS_NR::Restroom_Public",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Restroom_Public",
                "name": "2021::PHIUS_NR::Restroom_Public",
                "watts_per_m2": 2.906253,
            },
        },
    },
    "2021::PHIUS_NR::Department_Store": {
        "name": "Department Store",
        "hb_base_program": "2019::Retail::Core_Retail",
        "protocol": "PHIUS_NonRes",
        "description": "Retail shop/Department store",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::Retail::Core_Retail",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Department_Store",
                "identifier": "2021::PHIUS_NR::Department_Store",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Department_Store",
                "name": "2021::PHIUS_NR::Department_Store",
                "people_per_area": 0.161459,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Department_Store",
                "name": "2021::PHIUS_NR::Department_Store",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Department_Store",
                "name": "2021::PHIUS_NR::Department_Store",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Department_Store",
                "name": "2021::PHIUS_NR::Department_Store",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Department_Store",
                "name": "2021::PHIUS_NR::Department_Store",
                "watts_per_m2": 3.22917,
            },
        },
    },
    "2021::PHIUS_NR::Grocery": {
        "name": "Grocery",
        "hb_base_program": "2019::SuperMarket::Sales",
        "description": "Retail shop/department store (food department with refrigerated products)",
        "protocol": "PHIUS_NonRes",
        "description": "",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SuperMarket::Sales"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Grocery",
                "identifier": "2021::PHIUS_NR::Grocery",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Grocery",
                "name": "2021::PHIUS_NR::Grocery",
                "people_per_area": 0.086111,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Grocery",
                "name": "2021::PHIUS_NR::Grocery",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Grocery",
                "name": "2021::PHIUS_NR::Grocery",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Grocery",
                "name": "2021::PHIUS_NR::Grocery",
                "annual_utilization_factor": 0.606735,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Grocery",
                "name": "2021::PHIUS_NR::Grocery",
                "watts_per_m2": 10.979178,
            },
        },
    },
    "2021::PHIUS_NR::Storage_Archive": {
        "name": "Storage Archive",
        "hb_base_program": "2019::Warehouse::Fine",
        "protocol": "PHIUS_NonRes",
        "description": "Storeroom technical equipment room or archive",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Warehouse::Fine"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Storage_Archive",
                "identifier": "2021::PHIUS_NR::Storage_Archive",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.02,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Storage_Archive",
                "name": "2021::PHIUS_NR::Storage_Archive",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Storage_Archive",
                "name": "2021::PHIUS_NR::Storage_Archive",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Storage_Archive",
                "name": "2021::PHIUS_NR::Storage_Archive",
                "target_lux": 100,
                "target_lux_height": 0.8,
                "watts_per_m2": 7.427091,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Storage_Archive",
                "name": "2021::PHIUS_NR::Storage_Archive",
                "annual_utilization_factor": 0.427397,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Storage_Archive",
                "name": "2021::PHIUS_NR::Storage_Archive",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::School_Auditorium": {
        "name": "School Auditorium",
        "hb_base_program": "2019::SecondarySchool::Auditorium",
        "protocol": "PHIUS_NonRes",
        "description": "Lecture room, auditorium",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::SecondarySchool::Auditorium",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::School_Auditorium",
                "identifier": "2021::PHIUS_NR::School_Auditorium",
                "start_hour": 8,
                "end_hour": 18,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::School_Auditorium",
                "name": "2021::PHIUS_NR::School_Auditorium",
                "people_per_area": 1.614587,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::School_Auditorium",
                "name": "2021::PHIUS_NR::School_Auditorium",
                "daily_operating_hours": 12,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::School_Auditorium",
                "name": "2021::PHIUS_NR::School_Auditorium",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::School_Auditorium",
                "name": "2021::PHIUS_NR::School_Auditorium",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::School_Auditorium",
                "name": "2021::PHIUS_NR::School_Auditorium",
                "watts_per_m2": 4.951394,
            },
        },
    },
    "2021::PHIUS_NR::Theater_Seating": {
        "name": "Theater Seating",
        "hb_base_program": "2019::Courthouse::Courtroom",
        "protocol": "PHIUS_NonRes",
        "description": "Spectators and audience area of theaters and event locations",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::Courthouse::Courtroom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Theater_Seating",
                "identifier": "2021::PHIUS_NR::Theater_Seating",
                "start_hour": 19,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Seating",
                "name": "2021::PHIUS_NR::Theater_Seating",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Seating",
                "name": "2021::PHIUS_NR::Theater_Seating",
                "daily_operating_hours": 4,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Seating",
                "name": "2021::PHIUS_NR::Theater_Seating",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_m2": 12.91668,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Seating",
                "name": "2021::PHIUS_NR::Theater_Seating",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Seating",
                "name": "2021::PHIUS_NR::Theater_Seating",
                "watts_per_m2": 0,
            },
        },
    },
    "2021::PHIUS_NR::Theater_Lobby": {
        "name": "Theater Lobby",
        "hb_base_program": "2019::MediumOffice::Lobby",
        "protocol": "PHIUS_NonRes",
        "description": "Foyer (theaters and event locations)",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::MediumOffice::Lobby",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Theater_Lobby",
                "identifier": "2021::PHIUS_NR::Theater_Lobby",
                "start_hour": 19,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Lobby",
                "name": "2021::PHIUS_NR::Theater_Lobby",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Lobby",
                "name": "2021::PHIUS_NR::Theater_Lobby",
                "daily_operating_hours": 4,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Lobby",
                "name": "2021::PHIUS_NR::Theater_Lobby",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 9.041676,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Lobby",
                "name": "2021::PHIUS_NR::Theater_Lobby",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Lobby",
                "name": "2021::PHIUS_NR::Theater_Lobby",
                "watts_per_m2": 2.906253,
            },
        },
    },
    "2021::PHIUS_NR::Theater_Stage": {
        "name": "Theater Stage",
        "hb_base_program": "2019::MediumOffice::OpenOffice",
        "protocol": "PHIUS_NonRes",
        "description": "Stage (theaters and event locations)",
        "source": [
            "PHIUS_Certification_Guidebook_v3.02_N10",
            "2019::MediumOffice::OpenOffice",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_NR::Theater_Stage",
                "identifier": "2021::PHIUS_NR::Theater_Stage",
                "start_hour": 13,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Stage",
                "name": "2021::PHIUS_NR::Theater_Stage",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Stage",
                "name": "2021::PHIUS_NR::Theater_Stage",
                "daily_operating_hours": 10,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.6,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Stage",
                "name": "2021::PHIUS_NR::Theater_Stage",
                "target_lux": 1000,
                "target_lux_height": 0.8,
                "watts_per_m2": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_NR::Theater_Stage",
                "name": "2021::PHIUS_NR::Theater_Stage",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS_NR::Theater_Stage",
                "name": "2021::PHIUS_NR::Theater_Stage",
                "watts_per_m2": 10.333344,
            },
        },
    },
}

# Programs from:
# - PHIUS_Multi-Family_Calculator- 021.03.23.xls
PHIUS_MF_Calculator = {
    "2021::PHIUS_MF::Central_Restroom": {
        "name": "Central Restroom",
        "hb_base_program": "2019::SmallHotel::PublicRestroom",
        "protocol": "PHIUS_MultiFamily",
        "description": "Central Restroom",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::SmallHotel::PublicRestroom",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Central_Restroom",
                "identifier": "2021::PHIUS_MF::Central_Restroom",
                "start_hour": 11.2,
                "end_hour": 12.8,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Central_Restroom",
                "name": "2021::PHIUS_MF::Central_Restroom",
                "people_per_area": 0.030677,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Central_Restroom",
                "name": "2021::PHIUS_MF::Central_Restroom",
                "daily_operating_hours": 1.6,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Central_Restroom",
                "name": "2021::PHIUS_MF::Central_Restroom",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 9.687519375,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Central_Restroom",
                "name": "2021::PHIUS_MF::Central_Restroom",
                "annual_utilization_factor": 0.07,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Central_Restroom",
                "name": "2021::PHIUS_MF::Central_Restroom",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Common_Laundry": {
        "name": "Common Laundry",
        "hb_base_program": "2019::SmallHotel::Laundry",
        "protocol": "PHIUS_MultiFamily",
        "description": "Common Laundry",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::SmallHotel::Laundry",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Common_Laundry",
                "identifier": "2021::PHIUS_MF::Common_Laundry",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Laundry",
                "name": "2021::PHIUS_MF::Common_Laundry",
                "people_per_area": 0.112483,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Common_Laundry",
                "name": "2021::PHIUS_MF::Common_Laundry",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Laundry",
                "name": "2021::PHIUS_MF::Common_Laundry",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 7.534737292,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Common_Laundry",
                "name": "2021::PHIUS_MF::Common_Laundry",
                "annual_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Laundry",
                "name": "2021::PHIUS_MF::Common_Laundry",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Common_Mail": {
        "name": "Common Mail",
        "hb_base_program": "2019::MediumOffice::Lobby",
        "protocol": "PHIUS_MultiFamily",
        "description": "Common Mail",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::MediumOffice::Lobby",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Common_Mail",
                "identifier": "2021::PHIUS_MF::Common_Mail",
                "start_hour": 6,
                "end_hour": 18,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Mail",
                "name": "2021::PHIUS_MF::Common_Mail",
                "people_per_area": 0.112483,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Common_Mail",
                "name": "2021::PHIUS_MF::Common_Mail",
                "daily_operating_hours": 12,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Mail",
                "name": "2021::PHIUS_MF::Common_Mail",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 30.13894917,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Common_Mail",
                "name": "2021::PHIUS_MF::Common_Mail",
                "annual_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Mail",
                "name": "2021::PHIUS_MF::Common_Mail",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Common_Office": {
        "name": "Common Office",
        "hb_base_program": "2019::MidriseApartment::Office",
        "protocol": "PHIUS_MultiFamily",
        "description": "Common Office",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::MidriseApartment::Office",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Common_Office",
                "identifier": "2021::PHIUS_MF::Common_Office",
                "start_hour": 7.5,
                "end_hour": 16.5,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Office",
                "name": "2021::PHIUS_MF::Common_Office",
                "people_per_area": 0.011302,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Common_Office",
                "name": "2021::PHIUS_MF::Common_Office",
                "daily_operating_hours": 9,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Office",
                "name": "2021::PHIUS_MF::Common_Office",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 10.76391042,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Common_Office",
                "name": "2021::PHIUS_MF::Common_Office",
                "annual_utilization_factor": 0.375,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Common_Office",
                "name": "2021::PHIUS_MF::Common_Office",
                "watts_per_m2": 42.30216794,
            },
        },
    },
    "2021::PHIUS_MF::Storage_or_Equip": {
        "name": "Storage/Equip Room",
        "hb_base_program": "2019::LargeOffice::Storage",
        "protocol": "PHIUS_MultiFamily",
        "description": "Storage/Equip Room",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::LargeOffice::Storage",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Storage_or_Equip",
                "identifier": "2021::PHIUS_MF::Storage_or_Equip",
                "start_hour": 0,
                "end_hour": 1,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Storage_or_Equip",
                "name": "2021::PHIUS_MF::Storage_or_Equip",
                "people_per_area": 0.0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Storage_or_Equip",
                "name": "2021::PHIUS_MF::Storage_or_Equip",
                "daily_operating_hours": 1,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Storage_or_Equip",
                "name": "2021::PHIUS_MF::Storage_or_Equip",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 16.14586563,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Storage_or_Equip",
                "name": "2021::PHIUS_MF::Storage_or_Equip",
                "annual_utilization_factor": 0.0416,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Storage_or_Equip",
                "name": "2021::PHIUS_MF::Storage_or_Equip",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Elevator": {
        "name": "Elevator",
        "hb_base_program": "2019::LargeOffice::Elevator Shaft",
        "protocol": "PHIUS_MultiFamily",
        "description": "Elevator",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::LargeOffice::Elevator Shaft",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Elevator",
                "identifier": "2021::PHIUS_MF::Elevator",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Elevator",
                "name": "2021::PHIUS_MF::Elevator",
                "people_per_area": 0.0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Elevator",
                "name": "2021::PHIUS_MF::Elevator",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Elevator",
                "name": "2021::PHIUS_MF::Elevator",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 13.45488802,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Elevator",
                "name": "2021::PHIUS_MF::Elevator",
                "annual_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Elevator",
                "name": "2021::PHIUS_MF::Elevator",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Corridor": {
        "name": "Indoor Corridor",
        "hb_base_program": "2019::MidriseApartment::Corridor",
        "protocol": "PHIUS_MultiFamily",
        "description": "Indoor Corridor",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::MidriseApartment::Corridor",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Corridor",
                "identifier": "2021::PHIUS_MF::Corridor",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Corridor",
                "name": "2021::PHIUS_MF::Corridor",
                "people_per_area": 0.0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Corridor",
                "name": "2021::PHIUS_MF::Corridor",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Corridor",
                "name": "2021::PHIUS_MF::Corridor",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 5.381955208,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Corridor",
                "name": "2021::PHIUS_MF::Corridor",
                "annual_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Corridor",
                "name": "2021::PHIUS_MF::Corridor",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Multi_Purpose": {
        "name": "Multi-Purpose",
        "hb_base_program": "2019::SmallHotel::Meeting",
        "protocol": "PHIUS_MultiFamily",
        "description": "Multi-Purpose / Community",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::SmallHotel::Meeting",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Multi_Purpose",
                "identifier": "2021::PHIUS_MF::Multi_Purpose",
                "start_hour": 6,
                "end_hour": 18,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Multi_Purpose",
                "name": "2021::PHIUS_MF::Multi_Purpose",
                "people_per_area": 0.538196,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Multi_Purpose",
                "name": "2021::PHIUS_MF::Multi_Purpose",
                "daily_operating_hours": 12,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Multi_Purpose",
                "name": "2021::PHIUS_MF::Multi_Purpose",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 11.84030146,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Multi_Purpose",
                "name": "2021::PHIUS_MF::Multi_Purpose",
                "annual_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Multi_Purpose",
                "name": "2021::PHIUS_MF::Multi_Purpose",
                "watts_per_m2": 0.0,
            },
        },
    },
    "2021::PHIUS_MF::Workout_Room": {
        "name": "Workout Room",
        "hb_base_program": "2019::PrimarySchool::Gym",
        "protocol": "PHIUS_MultiFamily",
        "description": "Workout Room",
        "source": [
            "PHIUS_Multi-Family_Calculator- 021.03.23.xls",
            "2019::PrimarySchool::Gym",
        ],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Workout",
                "identifier": "2021::PHIUS_MF::Workout",
                "start_hour": 6,
                "end_hour": 22,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Workout",
                "name": "2021::PHIUS_MF::Workout",
                "people_per_area": 0.322917,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Workout",
                "name": "2021::PHIUS_MF::Workout",
                "daily_operating_hours": 16,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Workout",
                "name": "2021::PHIUS_MF::Workout",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 9.687519375,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Workout",
                "name": "2021::PHIUS_MF::Workout",
                "annual_utilization_factor": 0.667,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Workout",
                "name": "2021::PHIUS_MF::Workout",
                "watts_per_m2": 12.04,
            },
        },
    },
    "2021::PHIUS_MF::Stair": {
        "name": "Indoor Stair",
        "hb_base_program": "2019::MediumOffice::Stair",
        "protocol": "PHIUS_MultiFamily",
        "description": "Indoor Stairwell",
        "source": ["2019::MediumOffice::Stair"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS_MF::Stair",
                "identifier": "2021::PHIUS_MF::Stair",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Stair",
                "name": "2021::PHIUS_MF::Stair",
                "people_per_area": 0.0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Stair",
                "name": "2021::PHIUS_MF::Stair",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.305919,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Stair",
                "name": "2021::PHIUS_MF::Stair",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_m2": 5.274311,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS_MF::Stair",
                "name": "2021::PHIUS_MF::Stair",
                "annual_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS_MF::Stair",
                "name": "2021::PHIUS_MF::Stair",
                "watts_per_m2": 0.0,
            },
        },
    },
}

# -- Full Library
PHIUS_library = {}  # type: Dict[str, Dict]
PHIUS_library.update(PHIUS_Non_Res)
PHIUS_library.update(PHIUS_MF_Calculator)
