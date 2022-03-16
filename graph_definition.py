from guest_response import GuestResponse
from host_response import HostResponse
from constants import LANGUAGES, DIETARY_RESTRICTIONS
import numpy as np

from typing import List


def compute_distance_weight(zip_code_1, zip_code_2):
    return 1


def is_a_match(guest_response: GuestResponse, host_response: HostResponse):
    num_ppl_mask = (guest_response.num_adults + guest_response.num_kids <= host_response.max_num_ppl)
    is_kids_friendly_mask = (guest_response.num_kids == 0) or host_response.is_kids_friendly
    common_language_mask = (bool(set(guest_response.languages) & set(host_response.languages)))
    guest_vaccination_mask = guest_response.has_vaccination or (~host_response.asks_vaccination)
    host_vaccination_mask = host_response.has_vaccination or (~guest_response.asks_vaccination)
    transportation_mask = (~guest_response.asks_transportation) or host_response.provides_transportation
    dietary_restriction_mask = (len(host_response.dietary_accommodations) > 0) or (
                guest_response.dietary_restrictions == ['none'])
    pets_mask = (~guest_response.has_pets_allergies) or (~host_response.has_pets)

    match = (
            num_ppl_mask and
            is_kids_friendly_mask and
            common_language_mask and
            guest_vaccination_mask and
            host_vaccination_mask and
            transportation_mask and
            dietary_restriction_mask and
            pets_mask
    )
    return match


def compute_compatibility_weight(guest_response: GuestResponse,
                                 host_response: HostResponse,
                                 language_multiplier: float = 1,
                                 distance_multiplier: float = 1,
                                 num_ppl_multiplier: float = 1,
                                 kids_multiplier: float = 1,
                                 transportation_multiplier: float = 1,
                                 dietary_multiplier: float = 1,
                                 wait_time_multiplier: float = 1,
                                 ):
    match = is_a_match(guest_response, host_response)
    if match == False:
        weight = -1
    else:
        language_weight = len(set(guest_response.languages) & set(host_response.languages)) / len(LANGUAGES)
        distance_weight = compute_distance_weight(guest_response.zip_code, host_response.zip_code)
        num_ppl_weight = 1 / (host_response.max_num_ppl - guest_response.num_adults - guest_response.num_kids + 1)
        kids_weight = (
                host_response.is_kids_friendly * (guest_response.num_kids > 0) * 1 +
                (~host_response.is_kids_friendly) * (guest_response.num_kids == 0) * 1 +
                host_response.is_kids_friendly * (guest_response.num_kids == 0) * 0.5
        )
        transportation_weight = (
                host_response.provides_transportation * (guest_response.asks_transportation) * 1 +
                (~host_response.provides_transportation) * (~guest_response.asks_transportation) * 1 +
                host_response.provides_transportation * (~guest_response.asks_transportation) * 0.5
        )
        dietary_weight = (
                (guest_response.dietary_restrictions == ['none']) * (
                    len(host_response.dietary_accommodations) > 0) * 0.5 +
                (guest_response.dietary_restrictions == ['none']) * (
                            len(host_response.dietary_accommodations) == 0) * 1 +
                (guest_response.dietary_restrictions != ['none']) * (1 - len(
            set(guest_response.dietary_restrictions) - set(host_response.dietary_accommodations)
        ) / len(DIETARY_RESTRICTIONS)
                                                                     )
        )
        wait_time_weight = min(1, (host_response.days_since_response + guest_response.days_since_response) / 20)

        weight = (
                language_multiplier * language_weight +
                distance_multiplier * distance_weight +
                num_ppl_multiplier * num_ppl_weight +
                kids_multiplier * kids_weight +
                transportation_multiplier * transportation_weight +
                dietary_multiplier * dietary_weight +
                wait_time_multiplier * wait_time_weight
        )

    return weight


def compute_compatibility_matrix(guest_responses: List[GuestResponse],
                                 host_responses: List[HostResponse]):
    matrix = np.zeros((len(guest_responses), len(host_responses)))
    for i, guest_response in enumerate(guest_responses):
        for j, host_response in enumerate(host_responses):
            weight = compute_compatibility_weight(guest_response, host_response)
            if weight > 100:
                print('HUJA')
            matrix[i][j] = weight
    return matrix
