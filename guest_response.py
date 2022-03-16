from typing import List
import numpy as np

from constants import BERLIN_ZIP_CODES

class GuestResponse:
    def __init__(self,
                 zip_code: int,
                 num_adults: int,
                 num_kids: int,
                 languages: List[str],
                 has_vaccination: bool,
                 asks_vaccination: bool,
                 asks_transportation: bool,
                 has_pets_allergies: bool,
                 dietary_restrictions: List[str],
                 days_since_response: int = 0
                 ):
        self.zip_code = zip_code
        self.num_adults = num_adults
        self.num_kids = num_kids
        self.languages = languages
        self.has_vaccination = has_vaccination
        self.asks_vaccination = asks_vaccination
        self.asks_transportation = asks_transportation
        self.has_pets_allergies = has_pets_allergies
        self.dietary_restrictions = dietary_restrictions
        self.days_since_response = days_since_response

        self.validate_zipcode(self.zip_code)
        self.validate_num_adults(self.num_adults)

    def validate_zipcode(self, zip_code):
        assert zip_code in BERLIN_ZIP_CODES, f"Value Error: Unknown zip code {zip_code}"

    def validate_num_adults(self, num_adults):
        assert type(num_adults) in [int, np.int64], f"Value Error: Number of adults has to be integer and not {type(num_adults)}"
        assert num_adults < 20, f"Value Error: Number of adults ({num_adults}) is to high"
