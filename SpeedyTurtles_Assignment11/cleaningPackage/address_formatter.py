import re
import pandas as pd

class AddressFormatter:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def format_addresses(self) -> pd.DataFrame:
        if 'Full Address' in self.data.columns:
            # Apply clean_address to the 'Full Address' column using .loc to avoid SettingWithCopyWarning
            self.data.loc[:, 'Full Address'] = self.data['Full Address'].apply(self.clean_address)
        else:
            print("[WARNING] 'Full Address' column not found in the dataset. Skipping address formatting.")
        return self.data

    def clean_address(self, address: str) -> str:
        original_address = address

        # Remove excessive spaces and commas
        address = re.sub(r'\s*,\s*', ', ', address)  # Ensure one comma and space
        address = re.sub(r',+', ',', address)  # Remove multiple commas
        address = re.sub(r'\s+', ' ', address)  # Remove excessive spaces
        address = address.strip(', ')  # Remove leading/trailing commas and spaces

        # Split address into parts
        address_parts = [part.strip() for part in address.split(',')]

        # Initialize components
        street = ""
        city = ""
        state = ""
        zip_code = ""

        # Correct misplaced state and ZIP if they are at the beginning
        if len(address_parts) > 1 and re.match(r'^\d{5}\s+[A-Z]{2}$', address_parts[0]):
            zip_state_match = re.match(r'^(\d{5})\s+([A-Z]{2})$', address_parts.pop(0))
            if zip_state_match:
                zip_code, state = zip_state_match.groups()
        elif len(address_parts) > 1 and re.match(r'^[A-Z]{2}\s+\d{5}$', address_parts[0]):
            state_zip_match = re.match(r'^([A-Z]{2})\s+(\d{5})$', address_parts.pop(0))
            if state_zip_match:
                state, zip_code = state_zip_match.groups()

        # Process remaining parts to identify components
        for part in address_parts:
            # Check if part is a state abbreviation
            if re.match(r'^[A-Z]{2}$', part) and not state:
                state = part
            # Check if part is a ZIP code
            elif re.match(r'^\d{5}$', part) and not zip_code:
                zip_code = part
            # Assume the remaining part is the city if state is already found
            elif state and not city:
                city = part
            # Otherwise, it's part of the street address
            else:
                if street:
                    street = f"{street}, {part}"
                else:
                    street = part

        # Ensure the components are correctly placed in the address order: street, city, state, zip
        components = [street, city, state, zip_code]
        formatted_address = ', '.join([comp for comp in components if comp])

        # Print original and formatted address if they are different
        if original_address != formatted_address:
            print(f"[INFO] Address formatted: '{original_address}' -> '{formatted_address}'")
        
        return formatted_address
