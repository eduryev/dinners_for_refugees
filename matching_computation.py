from scipy.optimize import linear_sum_assignment
import pandas as pd

from graph_definition import compute_compatibility_matrix, is_a_match
from host_response import HostResponse
from guest_response import GuestResponse


guest_responses_df = pd.read_csv('sample_data/sample_guest_responses.csv')
host_responses_df = pd.read_csv('sample_data/sample_host_responses.csv')

guest_responses = []
for i in range(len(guest_responses_df)):
    guest_responses.append(GuestResponse(**dict(guest_responses_df.iloc[i])))

host_responses = []
for i in range(len(host_responses_df)):
    host_responses.append(HostResponse(**dict(host_responses_df.iloc[i])))
#%%
compatibility_matrix = compute_compatibility_matrix(guest_responses, host_responses)
compatibility_matrix
#%%
matched_guests, matched_hosts = linear_sum_assignment(compatibility_matrix, maximize=True)
len(matched_guests), len(matched_hosts)
#%%
