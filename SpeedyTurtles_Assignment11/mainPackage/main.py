

import os
from CSVPackage.CSVProcessor import CSVProcessor
from 

if __name__ == "__main__":
    api_key = "538220c0-a0fe-11ef-960a-33b50c08c2d9"  
    file_path = os.path.join(os.path.dirname(__file__), 'Data', 'fuelPurchaseData-1.csv')
    
    cleaner = FuelDataCleanerController(file_path, api_key)
    cleaner.clean_data()