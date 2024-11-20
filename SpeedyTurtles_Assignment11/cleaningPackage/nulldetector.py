import pandas as pd

class NullDetector:
    """Class to detect invalid rows in the 'Transaction Number' column."""

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def detect_nulls(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Detect anomalies in 'Transaction Number', distinguishing between numpy.nan, "nan" (string), and empty strings.
        Returns:
            - Cleaned DataFrame: Data without anomalies.
            - Anomalies DataFrame: Data with anomalies, unaltered.
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
