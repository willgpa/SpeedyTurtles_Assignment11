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
        self.file_path = file_path
        self.api_key = api_key
        self.csv_processor = CSVProcessor()
        self.data = self.csv_processor.load_csv(file_path)
        self.anomalies = pd.DataFrame()

    def clean_data(self):
        # Step 1: Detect anomalies in 'Transaction Number'
        null_detector = NullDetector(self.data)
        self.data, null_anomalies = null_detector.detect_nulls()
        print("After NullDetector - Cleaned Data:")
        print(self.data.head())
        print("After NullDetector - Anomalies:")
        print(null_anomalies.head())
        self.anomalies = pd.concat([self.anomalies, null_anomalies], ignore_index=True)

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

        # Save anomalies
        anomalies_file_path = os.path.join(os.path.dirname(self.file_path), 'dataAnomalies.csv')
        self.csv_processor.save_csv(self.anomalies, anomalies_file_path)

    