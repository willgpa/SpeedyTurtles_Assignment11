########################################################################################################################################################################
# Name: Will Padgett, Aryan Patel                                                                                                                                      #
# email:  padgetwg@mail.uc.edu, patel7ag@mail.uc.edu                                                                                                                   #
# Assignment Number: Assignment 11                                                                                                                                     #
# Due Date:   11/20/2024                                                                                                                                               # 
# Course #/Section: 4010/001                                                                                                                                           #
# Semester/Year:   1/4                                                                                                                                                 #
# Brief Description of the assignment: collaborate with peers to develop a VS project that cleans data from a CSV                                                      #
# Brief Description of what this module does: This module adds missing zip codes to the address information using an API                                               #                                       
#                                                                                                                                                                      #
# Citations: W3 Schools,GPT 4                                                                                                                                          #
# Anything else that's relevant:                                                                                                                                       #
########################################################################################################################################################################

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
        """
        Initializes the ZipCodeAdder with a DataFrame and an API key.

        @param data: DataFrame containing address data.
        @param api_key: API key for accessing the Zipcodebase API.
        """
        self.data = data
        self.api_key = api_key
        self.zip_cache = {}  # Cache for storing successful city/state -> ZIP mappings
        self.failed_requests = []  # Track addresses with consistent failures
        self.added_count = 0

    def add_zip_codes(self) -> pd.DataFrame:
        """
        Adds missing zip codes to the 'Full Address' column in the DataFrame using the Zipcodebase API.

        The method identifies addresses without zip codes, retrieves the missing zip codes using the API,
        and appends them to the existing addresses.

        @return: DataFrame with updated addresses containing zip codes.
        """
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
                    self.added_count+=1
        # Log any failures
        if self.failed_requests:
            print("Failed to retrieve zip codes for the following locations:")
            for city, state in self.failed_requests:
                print(f"{city}, {state}")
        
        return self.data

    def _extract_city_state(self, full_address):
        """
        Extracts and converts city and state from the full address string.

        @param full_address: The full address string to extract city and state from.
        @return: A tuple (city, state) if found, otherwise None.
        """
        address_parts = full_address.split(',')
        if len(address_parts) >= 2:
            city = address_parts[-2].strip()  # Extract city
            state_abbr = address_parts[-1].strip().split()[0]  # Extract state code
            state = self.STATE_ABBREVIATIONS.get(state_abbr.upper(), state_abbr)  # Convert to full state name
            return city, state
        return None

    def _get_zip_code_by_city(self, city, state):
        """
        Fetches a zip code for a given city and state using the Zipcodebase API with error handling.

        @param city: The name of the city.
        @param state: The full name of the state.
        @return: The zip code as a string if found, otherwise None.
        """
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
