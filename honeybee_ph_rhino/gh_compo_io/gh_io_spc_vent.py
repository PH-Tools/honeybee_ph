# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Component Interface for Create SpacePhVentFlows"""

try:
    from Grasshopper import DataTree
except ImportError:
    pass  # outside Grasshopper

try:
    from itertools import izip_longest
except:
    # Python 3+
    from itertools import zip_longest as izip_longest

from honeybee_ph_rhino import gh_io
from honeybee_ph_utils import input_tools
from honeybee_ph_rhino.gh_compo_io import ghio_validators


class SpacePhVentFlowRates(object):
    """Temporary dataclass to store flow-rate info"""
    v_sup = ghio_validators.FloatPositiveValue('v_sup')
    v_eta = ghio_validators.FloatPositiveValue('v_eta')
    v_tran = ghio_validators.FloatPositiveValue('v_tran')

    def __init__(self, _v_sup, _v_eta, _v_tran):
        # type: (float, float, float) -> None
        self.v_sup = _v_sup
        self.v_eta = _v_eta
        self.v_tran = _v_tran

    def __str__(self):
        return '{}(v_sup={:.2f}, v_eta={:.2f}, v_tran={:.2f})'.format(
            self.__class__.__name__, self.v_sup, self.v_eta, self.v_tran)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

# -----------------------------------------------------------------------------
# -- Component Interface


class ISpacePhVentFlows(object):

    def __init__(self, _IGH, _v_sups, _v_etas, _v_trans):
        # type: (gh_io.IGH, DataTree, DataTree, DataTree) -> None
        self.IGH = _IGH
        self.v_sup_tree = _v_sups
        self.v_eta_tree = _v_etas
        self.v_tran_tree = _v_trans

    def create_output(self):
        # type: () -> DataTree
        output = self.IGH.Grasshopper.DataTree[SpacePhVentFlowRates]()
        pth = self.IGH.Grasshopper.Kernel.Data.GH_Path

        for branch_num, branches in enumerate(
            izip_longest(
                self.v_sup_tree.Branches,
                self.v_eta_tree.Branches,
                self.v_tran_tree.Branches
            )
        ):
            # -- Any branch might be None, give empty list if so
            s, e, t = branches
            s = s or []
            e = e or []
            t = t or []

            # -- Build the output Branch based on the longest list input
            branch_len = max(len(s), len(e), len(t))
            for i in range(branch_len):
                output.Add(
                    SpacePhVentFlowRates(
                        input_tools.clean_get(s, i, 0.0),
                        input_tools.clean_get(e, i, 0.0),
                        input_tools.clean_get(t, i, 0.0)
                    ), pth(branch_num)
                )

        return output

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
