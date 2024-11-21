########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment: collaborate with peers to develop a VS project that cleans data from a CSV                                                      #
# Brief Description of what this module does: This module manages and orchestrates the data cleaning process                                                           #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools,GPT 4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################

import os
import pandas as pd

from CSVPackage.CSVProcessor import CSVProcessor
from cleaningPackage.duplicate_row_remover import DuplicateRowRemover
from cleaningPackage.gross_price_rounding import GrossPriceRounding
from cleaningPackage.non_fuel_filter import NonFuelFilter
from cleaningPackage.zip_code_adder import ZipCodeAdder
from cleaningPackage.nulldetector import NullDetector
from cleaningPackage.address_formatter import AddressFormatter


class DataController:
    def __init__(self, file_path, api_key):
        """
        Initializes the DataController with the file path to the CSV data and an API key for accessing zip code services.

        @param file_path: Path to the CSV file containing fuel purchase data.
        @param api_key: API key for the Zipcodebase API to retrieve zip codes for addresses.
        """
        self.file_path = file_path
        self.api_key = api_key
        self.csv_processor = CSVProcessor()
        self.data = self.csv_processor.load_csv(file_path)
        self.anomalies = pd.DataFrame()

    def clean_data(self):
        """
        Executes a series of data cleaning steps on the loaded fuel purchase data.

        The following steps are performed:
        1. Detect anomalies in the 'Transaction Number' column.
        2. Remove duplicate rows.
        3. Round values in the 'Gross Price' column to two decimal places.
        4. Filter out non-fuel types from the data.
        5. Add missing zip codes using the Zipcodebase API.
        6. Format addresses to ensure consistency.

        At the end of the process, a summary report is printed to show the counts of anomalies detected and modifications made.
        """

        null_detector = NullDetector(self.data)
        self.data, null_anomalies = null_detector.detect_nulls()
        print("After NullDetector - Cleaned Data:")
        print(self.data.head())
        print("After NullDetector - Anomalies:")
        print(null_anomalies.head())
        self.anomalies = pd.concat([self.anomalies, null_anomalies], ignore_index=True)

        # Step 2: Detect and remove negative 'Transaction Number' values
        print("\n[Step 2: Detect Negative Transaction Numbers]")
        self.data, negative_anomalies = null_detector.detect_negatives()

        # Check if `negative_anomalies` contains any rows
        if not negative_anomalies.empty:
            print(f"[DEBUG] Negative anomalies detected: {len(negative_anomalies)}")
            print(f"[DEBUG] Sample of negative anomalies:\n{negative_anomalies.head()}")

        # Add detected negative anomalies to self.anomalies
        if not negative_anomalies.empty:
            self.anomalies = pd.concat([self.anomalies, negative_anomalies], ignore_index=True)
            print(f"Total anomalies after adding negative anomalies: {len(self.anomalies)}")
        else:
            print("No negative anomalies detected.")

        # Add detected negative anomalies to self.anomalies
        self.anomalies = pd.concat([self.anomalies, negative_anomalies], ignore_index=True)

        # Step 2: Remove duplicates
        duplicate_remover = DuplicateRowRemover(self.data)
        self.data = duplicate_remover.remove_duplicates()

        # Step 3: Round 'Gross Price'
        price_rounder = GrossPriceRounding(self.data)
        self.data = price_rounder.round_price()

        # Step 4: Filter non-fuel purchases
        non_fuel_filter = NonFuelFilter(self.data)
        self.data, non_fuel_anomalies = non_fuel_filter.filter_non_fuel_types()
        self.anomalies = pd.concat([self.anomalies, non_fuel_anomalies], ignore_index=True)

        # Step 5: Add missing zip codes
        zip_code_adder = ZipCodeAdder(self.data, self.api_key)
        self.data = zip_code_adder.add_zip_codes()

        # Step 6: Format addresses
        address_formatter = AddressFormatter(self.data)
        self.data = address_formatter.format_addresses()

       
        # Save cleaned data
        cleaned_file_path = os.path.join(os.path.dirname(self.file_path), 'cleaned_fuel_data.csv')
        self.csv_processor.save_csv(self.data, cleaned_file_path)

        print("\n[SUMMARY REPORT]")
        print(f"Total null anomalies detected: {len(null_anomalies)}")
        print(f"Total duplicates removed: {duplicate_remover.removed_count if hasattr(duplicate_remover, 'removed_count') else 'Unknown'}")
        print(f"Total non-fuel anomalies filtered: {len(non_fuel_anomalies)}")
        print(f"Total zip codes added: {zip_code_adder.added_count if hasattr(zip_code_adder, 'added_count') else 'Unknown'}")
        print(f"Total addresses formatted: {address_formatter.formatted_count if hasattr(address_formatter, 'formatted_count') else 'Unknown'}")
        print("[End of Report]\n")