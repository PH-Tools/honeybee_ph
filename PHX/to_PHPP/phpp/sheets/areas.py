
class Areas:
    sheet_name = 'Areas'

    def __init__(self, _xl):
        """U-Values Worksheet

        Arguments:
        ----------
            * xl (excel_app.Connection): The Excel Connection / App to use 
        """

        self.xl = _xl
