

class U_Values:
    sheet_name = 'U-Values'

    def __init__(self, _xl):
        """Areas Worksheet

        Arguments:
        ----------
            * xl (excel_app.Connection): The Excel Connection / App to use 
        """

        self.xl = _xl
