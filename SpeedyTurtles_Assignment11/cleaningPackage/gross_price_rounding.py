import pandas as pd

class GrossPriceRounding:
    """Class to round 'Gross Price' to exactly two decimal places."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def round_price(self) -> pd.DataFrame:
        self.data['Gross Price'] = self.data['Gross Price'].round(2)
        return self.data

