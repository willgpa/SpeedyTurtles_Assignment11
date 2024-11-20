# Document here

import csv
import pandas as pd

class CSVProcessor:
    def load_csv(self, file_path):
        """
        Load a CSV while treating 'nan' as a string, not NaN.
        """
        return pd.read_csv(
            file_path,
            dtype={"Transaction Number": str},  # Force Transaction Number as string
            na_values=[],  # Disable automatic conversion of any values to NaN
            keep_default_na=False  # Keep default NaN handling off
        )

    def save_csv(self, data, file_path, is_anomalies=False):
        """
        Save the DataFrame to a CSV file. Avoid processing anomalies.
        :param data: DataFrame to save
        :param file_path: Path to save the CSV
        :param is_anomalies: Boolean indicating if the data is anomalies
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

