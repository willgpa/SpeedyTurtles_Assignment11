import pandas as pd
import requests

class ZipCodeAdder:
    """Class to add missing zip codes using an external API."""
    
    def __init__(self, data: pd.DataFrame, api_key: str):
        self.data = data
        self.api_key = api_key

    def add_zip_codes(self) -> pd.DataFrame:
        missing_zip = self.data[~self.data['Full Address'].str.contains(r'\d{5}', regex=True)]
        for index, row in missing_zip.iterrows():
            address_parts = row['Full Address'].split(',')
            if len(address_parts) >= 2:
                city = address_parts[0].strip()
                state = address_parts[1].strip().split()[0]
                zip_code = self._get_zip_code(city, state)
                if zip_code:
                    # Append zip code to the address
                    self.data.at[index, 'Full Address'] = row['Full Address'] + ' ' + zip_code
        return self.data

    def _get_zip_code(self, city, state):
        """Helper method to fetch a zip code for a given city and state using the ZipCodeBase API."""
        url = "https://app.zipcodebase.com/api/v1/search"
        params = {
            "apikey": self.api_key,
            "country": "US",
            "city": city,
            "state": state
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Return the first valid zip code
                return data['results'][0]['postal_code']
        return None

