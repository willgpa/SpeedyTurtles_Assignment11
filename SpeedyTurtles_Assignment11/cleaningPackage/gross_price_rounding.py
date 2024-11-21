########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment:collaborate with peers to develop a VS project Cleans data from a CSV                                                            #                                                                                                                                                                  
# Brief Description of what this module does.  This module make the price exactly 2 decimal places                                                                     #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools, GPT4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################

import pandas as pd

class GrossPriceRounding:
    """Class to round 'Gross Price' to exactly two decimal places."""
    
   
    def __init__(self, data: pd.DataFrame):
        """
        Initializes the GrossPriceRounding with a DataFrame.

        @param data: DataFrame that contains the 'Gross Price' column to be rounded.
        """
        self.data = data

    def round_price(self) -> pd.DataFrame:
        """
        Rounds the 'Gross Price' column to exactly two decimal places.

        The method converts the 'Gross Price' column to numeric, rounding the values to two decimal places,
        and formats them as strings with two decimal places.

        @return: DataFrame with the 'Gross Price' column rounded to two decimal places.
        """
        # Ensure the column is numeric
        self.data['Gross Price'] = pd.to_numeric(self.data['Gross Price'], errors='coerce')
        # Round and format as strings with two decimals
        self.data['Gross Price'] = self.data['Gross Price'].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "0.00")
        return self.data