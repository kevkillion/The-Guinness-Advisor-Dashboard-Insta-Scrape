
#--------------------------INSTA Scraper Project-------------------------------#
#------December 2022-----------#

# Import packages

import pandas as pd
import regex as re
from rich import print
from rich.pretty import pprint


# Fix variable types with Scientific Notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

#-------------------- IMPORT AND CLEAN DATA -------------------------------------#


df = pd.read_excel('instagram_guinnessadvisor_205x146.xlsx')

# Check for NULL/ na values
df_na = df.isnull().any()
df_na_columns = df.columns[df.isnull().any()]

# Drop empty columns
df_clean = df.dropna(axis=1, how='all')
print('\n NA Columns Dropped:\n', df_na_columns, headers='keys', tablefmt='psql')

# Drop columns based on string in column title
df_clean_2 = df[df_clean.columns.drop(list(df_clean.filter(
    regex='childPosts|mentions|latestComments|hashtags|dimensions|firstComment|images|displayUrl')))]
print('\n Immaterial Columns Dropped:', set(df_clean_2.columns) ^ set(df_clean.columns), '\n')

# Drop columns with same data in all rows
df_clean_3 = df_clean_2[[c for c in list(
    df_clean_2) if len(df_clean_2[c].unique()) > 1]]
print('Single Value Columns Dropped:', set(df_clean_3.columns) ^ set(df_clean_2.columns), '\n')

# Reorder Columns
df_clean_4 = df_clean_3.reindex(columns=['id', 'caption', 'rating', 'commentsCount', 'likesCount',
                                'shortCode', 'timestamp', 'type', 'url', 'videoUrl', 'videoViewCount'])
print('Final Columns List:\n', df_clean_3.columns, '\n')

# Export Dataframe to Excel
writer = pd.ExcelWriter('clean_instagram_guinnessadvisor.xlsx')
df_clean_4.to_excel(writer, index=False)
writer.save()

pprint('Dataframe cleaned and exported to Excel successfully')

#--------------------------- SET FUNCTIONS -----------------------------------#


# Function to get rating from caption
def find_rating(row):
    match = re.search(r'(\d+(\.\d+)?\/10)', row['caption'])
    if match:
        return match.group()
    else:
        return None

df_clean_4['rating'] = df_clean_4.apply(find_rating, axis=1)

# Function to get pub name from caption
def find_pub(caption):
    pattern = re.compile(r'(.*)\s(\d+(\.\d+)?\/10)')
    match = pattern.search(caption)
    if match:
        return match.group(1)
    return None

df_clean_4['pub'] = df_clean_4['caption'].apply(find_pub)

# Manual Overrides
df_clean_4['pub'] = df_clean_4['pub'].str.replace(r'\d[./]$', '') # Remove trailing numbers
df_clean_4.loc[df_clean_4['id'] == 2822241199869551744, 'pub'] = "The Annesley House"
df_clean_4.loc[df_clean_4['shortCode'] == 'BsK69j2HcND', 'pub'] = "Walsh's Stoneybatter"
df_clean_4.loc[df_clean_4['shortCode'] == 'BtbcYW7nRPH', 'pub'] = "Walsh's Pub Rush"

pprint('Manual Overrides completed successfully')

# Remove whitespace
def remove_whitespace(df, column_name):
    df[column_name] = df[column_name].str.strip()
    return df

df_final = remove_whitespace(df_clean_4, 'pub')

# Add Addresses
df_final['pub address'] = df_final['pub'] + ', Dublin, Ireland'


#--------------------------- SAVE AND WRITE TO EXCEL -----------------------------------#

# Export Final Output
writer = pd.ExcelWriter('final_instagram_guinnessadvisor.xlsx')
df_final.to_excel(writer, index=False)
writer.save()

pprint('New Dataframe fields created and exported to Excel successfully')


'''
Next Step - go to geocode.py python file. This file uses the googlemaps API 
to find longitude and latitude coordinates for addresses for each pub in the dataframe.
Make sure to set up API Key and enhance addresses as best possible

'''



