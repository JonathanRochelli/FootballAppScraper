from pymongo import MongoClient
from pprint import pprint
import requests
import json

# MongoDb configuration
client = MongoClient("localhost:27017")
db=client["football-app-db"]
countries = db["Countries"]

# Rapid API account configuration
headers = {
    'x-rapidapi-key': "e957d522eamshd2baa32faa95c3dp19d127jsna00de7e5175c",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

############################### Countries ###############################
# Get countries from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/countries"
football_api_countries = json.loads(requests.request("GET", url, headers=headers).text)["response"]

# Insert countries in MongoDB database
result = countries.insert_many(football_api_countries)
pprint(result)
