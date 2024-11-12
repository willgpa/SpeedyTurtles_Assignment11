import pandas as pd
import requests
import re

class ZipCodeAdder:
    """Class to add missing zip codes using Zipcodebase API with enhanced error handling and logging."""

    STATE_ABBREVIATIONS = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
        "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
        "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }

    def __init__(self, data: pd.DataFrame, api_key: str):
        self.data = data
        self.api_key = api_key
        self.zip_cache = {}  # Cache for storing successful city/state -> ZIP mappings
        self.failed_requests = []  # Track addresses with consistent failures

    def add_zip_codes(self) -> pd.DataFrame:
        # Pattern to detect existing 5-digit ZIP codes
        zip_code_pattern = re.compile(r'\b\d{5}\b')
        missing_zip = self.data[~self.data['Full Address'].str.contains(zip_code_pattern)]

        for index, row in missing_zip.iterrows():
            city_state = self._extract_city_state(row['Full Address'])
            if city_state:
                city, state = city_state

                # Check cache first
                if (city, state) in self.zip_cache:
                    zip_code = self.zip_cache[(city, state)]
                else:
                    zip_code = self._get_zip_code_by_city(city, state)
                    if zip_code:
                        self.zip_cache[(city, state)] = zip_code
                    else:
                        # Log failures for possible manual review
                        self.failed_requests.append((city, state))
                        continue

                # Append ZIP code to address if found
                if zip_code:
                    self.data.at[index, 'Full Address'] = f"{row['Full Address']} {zip_code}"

        # Log any failures
        if self.failed_requests:
            print("Failed to retrieve zip codes for the following locations:")
            for city, state in self.failed_requests:
                print(f"{city}, {state}")
        
        return self.data

    def _extract_city_state(self, full_address):
        """Extract and convert city and state to full state name if abbreviated."""
        address_parts = full_address.split(',')
        if len(address_parts) >= 2:
            city = address_parts[-2].strip()  # Extract city
            state_abbr = address_parts[-1].strip().split()[0]  # Extract state code
            state = self.STATE_ABBREVIATIONS.get(state_abbr.upper(), state_abbr)  # Convert to full state name
            return city, state
        return None

    def _get_zip_code_by_city(self, city, state):
        """Fetch a zip code for a city/state using the API, with enhanced error handling."""
        url = "https://app.zipcodebase.com/api/v1/code/city"
        headers = {"apikey": self.api_key}
        params = {
            "city": city,
            "country": "US",
            "state_name": state,
            "limit": 1  # Set a limit of 1 to retrieve only one ZIP code
        }

        for attempt in range(3):  # Attempt up to 3 times
            try:
                print(f"Attempting to fetch zip code for {city}, {state} (Attempt {attempt + 1})")
                response = requests.get(url, headers=headers, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('results') and len(data['results']) > 0:
                        zip_code = data['results'][0]
                        print(f"Zip code found for {city}, {state}: {zip_code}")
                        return zip_code
                    else:
                        print(f"No zip code found for {city}, {state} in API response.")
                        return None
                elif response.status_code == 403:
                    print(f"API access forbidden for {city}, {state}. Check API key and permissions.")
                    return None
                elif response.status_code == 404:
                    print(f"Data not found for {city}, {state}. Moving to next.")
                    return None
                else:
                    print(f"Unexpected status code {response.status_code} for {city}, {state}. Retrying...")

            except requests.exceptions.Timeout:
                print(f"Request timed out for {city}, {state}. Retrying...")
            except requests.exceptions.RequestException as e:
                print(f"Request error for {city}, {state}: {e}. Retrying...")

        print(f"Failed to fetch zip code for {city}, {state} after 3 attempts.")
        return None
