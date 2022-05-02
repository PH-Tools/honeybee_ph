# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller for managing the PHPP Connection."""

from PHX.to_PHPP.phpp import xl_app
from PHX.to_PHPP.phpp import sheets


class PHPPConnection:
    def __init__(self):
        # -- Setup the Excel connection and facade object.
        self.xl: xl_app.XLConnection = xl_app.XLConnection()

        # -- Setup all the individual worksheet Classes.
        self.u_values = sheets.UValues(self.xl)
        self.components = sheets.Components(self.xl)
        self.areas = sheets.Areas(self.xl, self.u_values)
