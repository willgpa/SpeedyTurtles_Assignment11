import pandas as pd

class DuplicateRowRemover:
    """Class to remove exact duplicate rows."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def remove_duplicates(self) -> pd.DataFrame:
        self.data.drop_duplicates(inplace=True)
        return self.data

