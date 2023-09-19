# Honeybee-PH:

Honeybee-PH is a free plugin for [Ladybug Tools](https://www.ladybug.tools/) which enables users to add detailed "Passive House" style attributes to their models in addition to the normal Honeybee inputs. Both Passive House Institute (PHI) and Passive House Institute US (Phius) model data can be added to the Ladybug-Tools models using the plugin. Note that this plugin is in no way affiliated with or created by either the Passive House Institute (PHI) or the Passive House Institute US (Phius).

This plugin is designed to be used as a plugin for Honeybee v1.5 or higher. It can also be utilized by the Ladybug toolkit for building up models using [Rhino 3D](https://www.rhino3d.com/) and Grasshopper using the [honeybee_grasshopper_ph](https://github.com/PH-Tools/honeybee_grasshopper_ph) tools.

## Packages:

- **honeybee_energy_ph:** Extend the Honeybee-Energy package with new Passive House style attributes for elements such as windows, hvac and construction assemblies.

- **honeybee_ph:** Extend the basic Honeybee package with important new Passive House specific elements such as interior spaces and Passive House certification thresholds.

- **honeybee_ph_standards:** Helpful new standards for programs and assemblies which are especially relevant to Passive House practitioners.

- **honeybee_ph_utils:** Some additional misc. utilities used by the above packages.

# More Information:

For more information on the use of these tools, check out the the Passive House Tools website:
http://www.PassiveHouseTools.com

In most cases, once the detailed Passive House style data has been added to the Ladybug-Tools / Honeybee model, practitioners will then want to export the model data out to either the Passive House Planning Package (PHPP) or WUFI-Passive. The Passive House Exchange (PHX) library has been created for this purpose. For more information on model data input / output, see the [PHX package](https://github.com/PH-Tools/PHX).

![Tests](https://github.com/PH-Tools/honeybee_ph/actions/workflows/ci.yaml/badge.svg)
[![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)
