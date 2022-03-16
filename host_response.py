from typing import List
import numpy as np

from constants import BERLIN_ZIP_CODES


class HostResponse:
    def __init__(self,
                 zip_code: int,
                 max_num_ppl: int,
                 is_kids_friendly: bool,
                 languages: List[str],
                 has_vaccination: bool,
                 asks_vaccination: bool,
                 provides_transportation: bool,
                 has_pets: bool,
                 dietary_accommodations: List[str],
                 days_since_response: int = 0
                 ):
        self.zip_code = zip_code
        self.max_num_ppl = max_num_ppl
        self.is_kids_friendly = is_kids_friendly
        self.languages = languages
        self.has_vaccination = has_vaccination
        self.asks_vaccination = asks_vaccination
        self.provides_transportation = provides_transportation
        self.has_pets = has_pets
        self.dietary_accommodations = dietary_accommodations
        self.days_since_response = days_since_response

        self.validate_zipcode(self.zip_code)
        self.validate_max_num_ppl(self.max_num_ppl)

    def validate_zipcode(self, zip_code):
        assert zip_code in BERLIN_ZIP_CODES, f"Value Error: Unknown zip code {zip_code}"

    def validate_max_num_ppl(self, max_num_ppl):
        assert type(max_num_ppl) in [int, np.int64], f"Value Error: Maximal number of people has to be integer and not {type(max_num_ppl)}"
        assert max_num_ppl < 20, f"Value Error: Maximal number of people ({max_num_ppl}) is to high"
