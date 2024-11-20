########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment: collaborate with peers to develop a VS project that cleans data from a CSV                                                      #
# Brief Description of what this module does: This module filters out non-fuel transactions from the data                                                              #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools, GPT4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################


import pandas as pd
import os
from typing import Tuple

class NonFuelFilter:
    """Class to filter out non-fuel types and save them as anomalies."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initializes the NonFuelFilter with a DataFrame.

        @param data: DataFrame that contains the fuel type data to be filtered.
        """
        self.data = data
        self.anomalies = pd.DataFrame()

    def filter_non_fuel_types(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Filters out non-fuel types from the DataFrame.

        The method separates fuel-related rows from non-fuel rows. Non-fuel rows are stored as anomalies for later analysis or saving.

        @return: A tuple containing:
            - DataFrame with only fuel-related rows.
            - DataFrame containing rows classified as non-fuel anomalies.
        """
        fuel_types = ['lng', 'gas', 'methanol', 'diesel','LNG', 'biodiesel', 'ethanol','kerosene', 'liquefied natural gas', 'liquefied natural gas','liquid natural gas', 'LNG','propane' ]  # Adjust this list as needed
        non_fuel_anomalies = self.data[~self.data['Fuel Type'].isin(fuel_types)]
        self.data = self.data[self.data['Fuel Type'].isin(fuel_types)]
        
        # Store anomalies for later saving
        self.anomalies = pd.concat([self.anomalies, non_fuel_anomalies])
        
        print(f"[INFO] Count of newly added fuel type anomalies: {len(non_fuel_anomalies)}")
        return self.data, self.anomalies

   