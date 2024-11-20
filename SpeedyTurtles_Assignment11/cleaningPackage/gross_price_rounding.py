import pandas as pd

class GrossPriceRounding:
    """Class to round 'Gross Price' to exactly two decimal places."""
    
   
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def round_price(self) -> pd.DataFrame:
        # Ensure the column is numeric
        self.data['Gross Price'] = pd.to_numeric(self.data['Gross Price'], errors='coerce')
        # Round and format as strings with two decimals
        self.data['Gross Price'] = self.data['Gross Price'].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")
        return self.data