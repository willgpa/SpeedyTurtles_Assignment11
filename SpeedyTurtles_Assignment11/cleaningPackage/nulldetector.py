########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment: collaborate with peers to develop a VS project that cleans data from a CSV                                                      #
# Brief Description of what this module does: This module detects null values in specified columns of the data                                                         #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools,GPT 4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################


import pandas as pd

class NullDetector:
    """Class to detect invalid rows in the 'Transaction Number' column."""

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def detect_nulls(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Detects anomalies in the 'Transaction Number' column, including numpy.nan, "nan" (string), empty strings, 
        and negative values. The anomalies are returned separately from the cleaned data.

        @return: A tuple containing:
            - DataFrame with anomalies removed (cleaned data).
            - DataFrame containing only the rows with anomalies (invalid or missing values).
        """
        # Define invalid string representations
        invalid_strings = {"Null", "null", "nan", ""}

        # Identify anomalies
        invalid_rows = self.data[
            self.data['Transaction Number'].isnull() |  # Detect numpy.nan
            (self.data['Transaction Number'].astype(str).str.strip().str.lower().isin(invalid_strings))  # Detect invalid strings
        ]

        try:
            transaction_numbers_numeric = pd.to_numeric(self.data['Transaction Number'], errors='coerce')
            negative_rows = self.data[transaction_numbers_numeric < 0]
        except Exception as e:
            print(f"[WARNING] Error converting 'Transaction Number' to numeric: {e}")
            negative_rows = pd.DataFrame()

        # Combine anomalies from nulls/invalid strings and negative values
        anomalies = pd.concat([invalid_rows, negative_rows]).drop_duplicates()


        # Separate anomalies (unaltered)
        anomalies = invalid_rows.copy()

        # Remove anomalies from the cleaned data
        cleaned_data = self.data.drop(invalid_rows.index, errors='ignore')

        return cleaned_data, anomalies
