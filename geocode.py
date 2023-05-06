
#-------------------------- Geocode -------------------------------#
#------December 2022-----------#

import pandas as pd
import requests
import logging
import time

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

#------------------ CONFIGURATION -------------------------------

# Set your Google API key here. 
# Even if using the free 2500 queries a day, its worth getting an API key since the rate limit is 50 / second.
# With API_KEY = None, you will run into a 2 second delay every 10 requests or so.
# With a "Google Maps Geocoding API" key from https://console.developers.google.com/apis/, 
# the daily limit will be 2500, but at a much faster rate.
# Example: API_KEY = 'AIzaSyC9azed9tLdjpZNjg2_kVePWvMIBq154eA'
API_KEY = 'AIzaSyCO_M3417emHUS-cHUXh-BHzeS4smftSj8'
# Backoff time sets how many minutes to wait between google pings when your API limit is hit
BACKOFF_TIME = 30
# Set your output file name here.
output_filename = 'geocode_addresses.xlsx'
# Set your input file here
input_filename = "final_instagram_guinnessadvisor.xlsx"
# Specify the column name in your input data that contains addresses here
address_column_name = "pub address"
# Return Full Google Results? If True, full JSON results from Google are included in output
RETURN_FULL_RESULTS = False

#------------------ DATA LOADING --------------------------------

# Read the data to a Pandas Dataframe
data = pd.read_excel(input_filename)

if address_column_name not in data.columns:
	raise ValueError("Missing Address column in input data")

# Form a list of addresses for geocoding:
# Make a big list of all of the addresses to be processed.
addresses = data[address_column_name].tolist()

# **** DEMO DATA / IRELAND SPECIFIC! ****
# We know that these addresses are in Ireland, and there's a column for county, so add this for accuracy. 
# (remove this line / alter for your own dataset)
#addresses = (data[address_column_name] + ',' + data['County'] + ',Ireland').tolist()


#------------------	FUNCTION DEFINITIONS ------------------------

def get_google_results(address, api_key=None, return_full_response=False):
    """
    Get geocode results from Google Maps Geocoding API.
    
    Note, that in the case of multiple google geocode reuslts, this function returns details of the FIRST result.
    
    @param address: String address as accurate as possible. For Example "18 Grafton Street, Dublin, Ireland"
    @param api_key: String API key if present from google. 
                    If supplied, requests will use your allowance from the Google API. If not, you
                    will be limited to the free usage of 2500 requests per day.
    @param return_full_response: Boolean to indicate if you'd like to return the full response from google. This
                    is useful if you'd like additional location details for storage or parsing later.
    """
    # Set up your Geocoding url
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
    if api_key is not None:
        geocode_url = geocode_url + "&key={}".format(api_key)
        
    # Ping google for the reuslts:
    results = requests.get(geocode_url)
    # Results will be in JSON format - convert to dict using requests functionality
    results = results.json()
    
    # if there's no results or an error, return empty results.
    if len(results['results']) == 0:
        output = {
            "formatted_address" : None,
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "google_place_id": None,
            "type": None,
            "postcode": None
        }
    else:    
        answer = results['results'][0]
        output = {
            "formatted_address" : answer.get('formatted_address'),
            "latitude": answer.get('geometry').get('location').get('lat'),
            "longitude": answer.get('geometry').get('location').get('lng'),
            "accuracy": answer.get('geometry').get('location_type'),
            "google_place_id": answer.get("place_id"),
            "type": ",".join(answer.get('types')),
            "postcode": ",".join([x['long_name'] for x in answer.get('address_components') 
                                  if 'postal_code' in x.get('types')])
        }
        
    # Append some other details:    
    output['input_string'] = address
    output['number_of_results'] = len(results['results'])
    output['status'] = results.get('status')
    if return_full_response is True:
        output['response'] = results
    
    return output

#------------------ PROCESSING LOOP -----------------------------

# Ensure, before we start, that the API key is ok/valid, and internet access is ok
test_result = get_google_results("London, England", API_KEY, RETURN_FULL_RESULTS)
if (test_result['status'] != 'OK') or (test_result['formatted_address'] != 'London, UK'):
    logger.warning("There was an error when testing the Google Geocoder.")
    raise ConnectionError('Problem with test results from Google Geocode - check your API key and internet connection.')

# Create a list to hold results
results = []
# Go through each address in turn
for address in addresses:
    # While the address geocoding is not finished:
    geocoded = False
    while geocoded is not True:
        # Geocode the address with google
        try:
            geocode_result = get_google_results(address, API_KEY, return_full_response=RETURN_FULL_RESULTS)
        except Exception as e:
            logger.exception(e)
            logger.error("Major error with {}".format(address))
            logger.error("Skipping!")
            geocoded = True
            
        # If we're over the API limit, backoff for a while and try again later.
        if geocode_result['status'] == 'OVER_QUERY_LIMIT':
            logger.info("Hit Query Limit! Backing off for a bit.")
            time.sleep(BACKOFF_TIME * 60) # sleep for 30 minutes
            geocoded = False
        else:
            # If we're ok with API use, save the results
            # Note that the results might be empty / non-ok - log this
            if geocode_result['status'] != 'OK':
                logger.warning("Error geocoding {}: {}".format(address, geocode_result['status']))
            logger.debug("Geocoded: {}: {}".format(address, geocode_result['status']))
            results.append(geocode_result)           
            geocoded = True

    # Print status every 100 addresses
    if len(results) % 100 == 0:
    	logger.info("Completed {} of {} address".format(len(results), len(addresses)))
            
    # Every 500 addresses, save progress to file(in case of a failure so you have something!)
if len(results) % 500 == 0:
    pd.DataFrame(results).to_csv("{}_bak".format(output_filename))

# All done
logger.info("Finished geocoding all addresses")
# Write the full results to csv using the pandas library.
pd.DataFrame(results).to_excel(output_filename)



#---------------------------------------------------------------------------------------#
#--------------------------- POSTCODE SPLIT FUNCTION -----------------------------------#


import re
from rich.pretty import pprint

geocoded_df = pd.read_excel(output_filename)

pattern = r'D(\d{1,2})'

# Create function to extract postcode number and store as an integer
def extract_postcode(postcode):
    if isinstance(postcode, str):  # check if input is a string
        match = re.search(pattern, postcode)
        if match is not None :
            return int(match.group(1))
        else:
            return None
    else:
        return None

# Apply extract_postcode function to the 'postcode' column
geocoded_df['postcode_split'] = geocoded_df['postcode'].apply(extract_postcode)

pprint('Postcode extract function executed successfully')


# Create function to determine North or South Dublin based on postcode_split
def area_allocation(postcode_split):
    if postcode_split is not None:
        if postcode_split % 2 == 0:
            return 'South Dublin'
        else:
            return 'North Dublin'
    else:
        return None

# Apply area function to 'postcode_split' column
geocoded_df['area'] = geocoded_df['postcode_split'].apply(area_allocation)

pprint('North / South allocation function executed successfully')
print(geocoded_df['area'])

# Export Final Output
writer = pd.ExcelWriter('geocode_addresses.xlsx')
geocoded_df.to_excel(writer, index=False)
writer.save()

pprint('Updated geocode_addresses file exported to Excel successfully')



#------------------	JOIN RESULTS TO ORIGINAL DATAFRAME ------------------------

'''
Next Step - go to join.py python file. This file uses pandas merge function to left join
the geocoded coordinates and new formatted addresses into the final Excel file.

'''

