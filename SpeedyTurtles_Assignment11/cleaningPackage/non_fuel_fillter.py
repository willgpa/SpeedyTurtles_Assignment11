import pandas as pd
import os

class NonFuelFilter:
    """Class to filter out non-fuel types and save them as anomalies."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.anomalies = pd.DataFrame()

    def filter_non_fuel_types(self) -> (pd.DataFrame, pd.DataFrame):
        fuel_types = ['lng', 'gas', 'methanol', 'diesel']  # Adjust this list as needed
        non_fuel_anomalies = self.data[~self.data['Fuel Type'].isin(fuel_types)]
        self.data = self.data[self.data['Fuel Type'].isin(fuel_types)]
        
        # Store anomalies for later saving
        self.anomalies = pd.concat([self.anomalies, non_fuel_anomalies])
        return self.data, self.anomalies

    def save_anomalies(self, folder='data'):
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.anomalies.to_csv(os.path.join(folder, 'dataAnomalies.csv'), index=False)

