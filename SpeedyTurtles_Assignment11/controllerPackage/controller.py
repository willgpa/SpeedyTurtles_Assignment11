import os
import pandas as pd

from CSVPackage.CSVProcessor import CSVProcessor
from cleaningPackage.duplicate_row_remover import DuplicateRowRemover
from cleaningPackage.gross_price_rounding import GrossPriceRounding
from cleaningPackage.non_fuel_filter import NonFuelFilter
from cleaningPackage.zip_code_adder import ZipCodeAdder

class DataController:
    def __init__(self, file_path, api_key):
        self.file_path = file_path
        self.api_key = api_key
        self.csv_processor = CSVProcessor()
        self.data = self.csv_processor.load_csv(file_path)
        self.anomalies = pd.DataFrame()

    def clean_data(self):
        # Step 1: Round 'Gross Price' to two decimal places
        price_rounder = GrossPriceRounding(self.data)
        self.data = price_rounder.round_price()

        # Step 2: Remove exact duplicates
        duplicate_remover = DuplicateRowRemover(self.data)
        self.data = duplicate_remover.remove_duplicates()

        # Step 3: Filter out non-fuel purchases
        non_fuel_filter = NonFuelFilter(self.data)
        self.data, self.anomalies = non_fuel_filter.filter_non_fuel_types()
        self.save_anomalies()

        # Step 4: Add missing zip codes to addresses
        zip_code_adder = ZipCodeAdder(self.data, self.api_key)
        self.data = zip_code_adder.add_zip_codes()

        # Save cleaned data to CSV
        cleaned_file_path = os.path.join(os.path.dirname(self.file_path), 'cleaned_fuel_data.csv')
        self.csv_processor.save_csv(self.data, cleaned_file_path)

    def save_anomalies(self, folder='Data'):
        """Save anomalies to a CSV file."""
        anomalies_file_path = os.path.join(folder, 'dataAnomalies.csv')
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.csv_processor.save_csv(self.anomalies, anomalies_file_path)
