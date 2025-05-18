# Weatherbit.io API Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.getenv('WEATHERBIT_API_KEY')
API_ENDPOINT = os.getenv('WEATHERBIT_API_ENDPOINT')

# Default city for weather updates
DEFAULT_CITY = 'Patiala'
DEFAULT_COUNTRY = 'India'

# Units for weather data (M/S/I)
UNITS = 'M'  # M for Metric (Celsius, m/s, mm)
           # S for Scientific (Kelvin, m/s, mm)
           # I for Imperial (Fahrenheit, mph, in)

# Language for weather descriptions
LANGUAGE = 'en'  # English

# Update frequency (in minutes)
UPDATE_INTERVAL = 10  # Weather data updates every 5-10 minutes