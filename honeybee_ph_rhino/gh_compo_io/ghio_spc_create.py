# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Component Interface for HBPH - Create Spaces"""


try:
    from typing import Tuple
except ImportError:
    pass  # IronPython 2.7

try:
    from Grasshopper import DataTree
except ImportError:
    pass  # outside Grasshopper

try:
    from System import Object, Double, String
except:
    pass  # outside .NET

from ladybug_rhino.fromgeometry import from_face3d

from honeybee_ph import space
from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.make_spaces import make_floor, make_volume


class ICreateSpaces(object):

    def __init__(self,
                 _IGH,
                 _flr_seg_geom,
                 _weighting_factors,
                 _volume_geometry,
                 _volume_heights,
                 _space_names,
                 _space_numbers,
                 _space_ph_vent_rates
                 ):
        # type: (gh_io.IGH, DataTree, DataTree, DataTree, DataTree, DataTree, DataTree, DataTree) -> None
        self.IGH = _IGH
        self.flr_geom = _flr_seg_geom
        self.weighting_factors = _weighting_factors
        self.vol_geom = _volume_geometry
        self.vol_heights = _volume_heights
        self.names = _space_names
        self.number = _space_numbers
        self.vent_rates = _space_ph_vent_rates

    def _clean_input_tree(self, _input_tree, branch_count, default, _type=Object):
        # type (DataTree, int, Any, Any) -> DataTree[<type>]
        """Align the input DataTrees so they are all the same length. Apply defaults."""

        new_tree = self.IGH.Grasshopper.DataTree[_type]()
        pth = self.IGH.Grasshopper.Kernel.Data.GH_Path
        for i in range(branch_count):
            try:
                new_tree.AddRange(_input_tree.Branch(i), pth(i))
            except ValueError:
                new_tree.Add(default, pth(i))
        return new_tree

    def create_output(self):
        # type: () -> Tuple
        # ------------------------------------------------------------------------------
        # -- Organize the input trees, lists, lengths, defaults
        input_len = len(self.flr_geom.Branches)
        weighting_factors = self._clean_input_tree(
            self.weighting_factors, input_len, 1.0, Double)
        volume_heights = self._clean_input_tree(self.vol_heights, input_len, 2.5, Double)
        space_names = self._clean_input_tree(self.names, input_len, '_Unnamed_', String)
        space_numbers = self._clean_input_tree(self.number, input_len, '000', String)
        vent_rates = self._clean_input_tree(self.vent_rates, input_len, None, Object)

        # ------------------------------------------------------------------------------
        spaces_ = []
        error_ = None
        floor_breps_ = DataTree[Object]()
        volume_breps_ = DataTree[Object]()
        # -- Build one Space for each branch on the _flr_seg_geom input tree
        for i, flr_srfc_list in enumerate(self.flr_geom.Branches):
            new_space = space.Space()
            new_space.name = space_names.Branch(i)[0]
            new_space.number = space_numbers.Branch(i)[0]

            space_floors, e = make_floor.space_floor_from_rh_geom(
                self.IGH, list(flr_srfc_list),
                list(weighting_factors.Branch(i))
            )
            if e:
                error_ = [from_face3d(s) for s in e]
                msg = 'Error: There was a problem joining together one or more group of floor surfaces?\n'\
                    'Check the "error_" output for a preview of the surfaces causing the problem\n'\
                    'Check the names and numbers of the surfaces, and make sure they can be properly merged?'
                self.IGH.error(msg)

            space_volumes = make_volume.volumes_from_floors(
                self.IGH, space_floors, list(volume_heights.Branch(i)))
            new_space.add_new_volumes(space_volumes)

            # -- Add any user-determined vent flow rates, if any
            try:
                flow_rate_obj = sum(vent_rates.Branch(i))
                new_space.properties.ph._v_sup = flow_rate_obj.v_sup
                new_space.properties.ph._v_eta = flow_rate_obj.v_eta
                new_space.properties.ph._v_tran = flow_rate_obj.v_tran
            except TypeError:
                pass

            spaces_.append(new_space)

            # -- Output Preview
            pth = self.IGH.Grasshopper.Kernel.Data.GH_Path
            floor_breps_.AddRange([from_face3d(flr.geometry)
                                  for flr in space_floors], pth(i))
            for srfc_list in [self.IGH.convert_to_rhino_geom(vol.geometry) for vol in space_volumes]:
                vol_brep = self.IGH.ghpythonlib_components.BrepJoin(srfc_list).breps
                volume_breps_.Add(vol_brep, pth(i))

        spaces_ = sorted(spaces_, key=lambda sp: sp.full_name)

        return error_, floor_breps_, volume_breps_, spaces_
