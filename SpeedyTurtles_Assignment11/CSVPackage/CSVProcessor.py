# Document here

import csv
import pandas as pd

class CSVProcessor:
    def load_csv(self, file_path):
         
         return pd.read_csv(file_path, low_memory=False)

    def save_csv(self, data, file_path):
        data.to_csv(file_path, index=False)
