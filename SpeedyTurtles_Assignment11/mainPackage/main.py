

import os
from CSVPackage.CSVProcessor import *
from controllerPackage.controller import DataController

if __name__ == "__main__":
    api_key = "538220c0-a0fe-11ef-960a-33b50c08c2d9"  
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'fuelPurchaseData-1.csv')
    print(f"File path: {file_path}")  # Check if the path is correct
    print(f"File exists: {os.path.exists(file_path)}")  # Check if the file actually exists

    # Initialize and run the cleaner
    cleaner = DataController(file_path, api_key)
    cleaner.clean_data()