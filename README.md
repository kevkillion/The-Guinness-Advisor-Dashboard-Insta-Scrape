
![Guinness Advisor Tableau Image](https://user-images.githubusercontent.com/65492956/230768902-1c5af60d-627b-4411-9d4e-58fa7e09e437.jpg)

**TABLEAU PUBLIC** - Check it out:

https://public.tableau.com/app/profile/kevin.killion/viz/Guinness_Advisor_Dark/DashboardDark

# **Instagram Guinness Advisor Data Extraction, Geocoding & Tableau Visualisation** 
This is a project that demonstrates how to scrape and analyse Instagram data using Apify, Python, and Google Maps API, and then visualize it using Tableau. The project involves scraping Instagram data from a specific profile, data cleansing, data enriching, geocoding and data visualisation.

# Prerequisites 💻
To run the this project, you will need to have the following software installed:

- Python 3.x
- Apify account
- Google Maps API key
- Tableau Desktop

Packages

```python 
import pandas as pd
import regex as re
from rich.pretty import pprint
import requests
import logging
import time
```

# Getting Started 🛠
To run the Python files in this project, follow these steps:

1. Clone this repository to your local machine.
2. Install the required Python libraries using pip.
3. Place the Apify output file (instagram_guinnessadvisor.xlsx) in the project directory.
4. Run the following command to clean the resulting data:

    **main.py**

5. Run the following command to geocode the address field

     **geocode.py**

6. Run the following command to join the cleaned data with the geocode data and produce a geocoded output file:

    **join.py**

The resulting file (final_instagram_guinnessadvisor_geocoded.xlsx) can be used for data visualization in Tableau or other similar visualtion tools.

# Data Extraction 🔑
The Apify application was used to extract Instagram posts tagged with the hashtag #GuinnessAdvisor. The extracted data included the post's caption, date, and location, as well as the number of likes and comments.

# Data Cleaning 🧼
The extracted data was cleaned using Python's Pandas library to remove any duplicate posts, and to reformat the date and time columns for easier analysis.

# Geocoding 🗺
The original data was also joined with geocoded addresses using Python's Pandas library. The geocoded data was then exported to a new file, ready for data visualization in Tableau or Power BI.

# Data Analysis 📊
The cleaned data was then loaded into Tableau, where a dashboard was created to analyze the data. The dashboard included visualizations of the total number of posts, likes, and comments, as well as the top ratings and locations.


# Files
The following files were used in this project:

- README.md: Description file outlining the project
- main.py: Python script for manipulating and cleansing data from exported Instagram data using the Apify application
- geocode.py: Python script for enriching address information and identifying longitude and latitude coordinates
- join.py: Python script for joining the cleaned data with geocoded addresses
- final_instagram_guinnessadvisor.xlsx: The cleaned data file
- geocode_addresses.xlsx: The geocoded addresses file
- final_instagram_guinnessadvisor_geocoded.xlsx: The final cleaned, geocoded data file 
- Instagram Guinness Advisor Dashboard.twbx: The Tableau dashboard file

# Conclusion
This project demonstrates the power of Python and Tableau in extracting, clensing and analyzing data from popular media platfroms. By using these tools, I was able to present information from Instagram in a dynamic, fun and visually aesthetic dashboard.


