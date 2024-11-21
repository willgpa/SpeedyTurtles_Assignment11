########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment: collaborate with peers to develop a VS project that cleans data from a CSV                                                      #
# Brief Description of what this module does: This module removes exact duplicate rows from the data                                                                   #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools, GPT4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################

import pandas as pd

class DuplicateRowRemover:
    """Class to remove exact duplicate rows."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initializes the DuplicateRowRemover with a DataFrame.

        @param data: DataFrame that contains the data from which duplicate rows need to be removed.
        """
        self.data = data
        self.removed_count = 0  # Initialize counter to track removed duplicates

    def remove_duplicates(self) -> pd.DataFrame:
        """
        Removes exact duplicate rows from the DataFrame and updates the removed count.

        @return: DataFrame with duplicate rows removed.
        """
        initial_count = len(self.data)
        self.data.drop_duplicates(inplace=True)
        self.removed_count = initial_count - len(self.data)  # Calculate the number of duplicates removed
        return self.data
