
# #------------------	JOIN RESULTS TO ORIGINAL DATAFRAME ------------------------

import pandas as pd
from rich.pretty import pprint

# Read files to be Joined
geocode_df = pd.read_excel('geocode_addresses.xlsx')
final_df = pd.read_excel('final_instagram_guinnessadvisor.xlsx')

# Left Join in Column
merged_df = pd.merge(final_df, geocode_df[['input_string', 'latitude', 'longitude', 'formatted_address', 'postcode', 'area']], 
                     left_on='pub address', right_on='input_string', how='left')

merged_df.drop('input_string', axis=1, inplace=True)
merged_df.drop_duplicates(subset=['caption','longitude','latitude','pub address'], inplace=True)

# Save Final File
merged_df.to_excel('final_instagram_guinnessadvisor_geocoded.xlsx', index=False)

pprint('Geocode file and final file joined successfully')

'''
This is the final step - Final file exported to excel is noted as 
final_instagram_guinnessadvisor_geocoded.xlsx. 

This file is ready for data visualisation in Tableau / Power BI

'''
