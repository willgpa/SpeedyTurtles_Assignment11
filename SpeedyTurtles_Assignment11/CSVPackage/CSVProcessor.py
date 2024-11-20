########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment: collaborate with peers to develop a VS project that cleans data from a CSV                                                      #
# Brief Description of what this module does: This module provides utilities for processing CSV files, including loading and saving                                    #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools,GPT 4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################

import csv
import pandas as pd

class CSVProcessor:
    def load_csv(self, file_path):
        """
        Loads a CSV file while treating 'nan' as a string, not as NaN.

        @param file_path: Path to the CSV file to be loaded.
        @return: DataFrame containing the loaded CSV data.
        """
        return pd.read_csv(
            file_path,
            dtype={"Transaction Number": str},  # Force Transaction Number as string
            na_values=[],  # Disable automatic conversion of any values to NaN
            keep_default_na=False  # Keep default NaN handling off
        )

    def save_csv(self, data, file_path, is_anomalies=False):
        """
        Saves the DataFrame to a CSV file. Handles specific columns like 'Gross Price' to ensure consistent formatting.

        @param data: DataFrame to save to CSV.
        @param file_path: Path where the CSV file should be saved.
        @param is_anomalies: Boolean indicating if the data is anomalies, which may skip certain processing steps.
        """
        # Create a copy of the DataFrame to avoid modifying the original
        data = data.copy()

        if not is_anomalies:
            # Ensure 'Gross Price' column exists
            if 'Gross Price' in data.columns:
                # Convert to numeric first to handle any invalid entries
                data['Gross Price'] = pd.to_numeric(data['Gross Price'], errors='coerce')

                # Convert to strings with two decimal places
                data['Gross Price'] = data['Gross Price'].apply(
                    lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00"
                )

        # Save the DataFrame to a CSV file
        print(f"Saving data to {file_path}...")
        print(data.head(10))
        data.to_csv(file_path, index=False, quoting=1)  # Force quoting for strings

