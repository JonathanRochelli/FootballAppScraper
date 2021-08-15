from pymongo import MongoClient
from pprint import pprint
from time import strftime
import requests
import json

with open('conf/conf.json') as f:
    conf = json.load(f)

# MongoDb configuration
client = MongoClient("{}:{}".format(conf["host"], conf["port"]))
db=client[conf["db"]]
countries = db["Countries"] # Countries collection
leagues = db["Leagues"] # Leagues collection
fixtures = db["Fixtures"] # Fixtures collection

with open('conf/key.json') as f:
    key = json.load(f)

# Rapid API account configuration
headers = {
    'x-rapidapi-key': key["key"],
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

############################### Countries ###############################
# Get countries from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/countries"
football_api_countries = json.loads(requests.request("GET", url, headers=headers).text)["response"]
# Remove all document in collection
countries.delete_many({})
# Insert countries in MongoDB database
result = countries.insert_many(football_api_countries)
pprint(result)

############################### Leagues ###############################
# Get leagues from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
football_api_leagues = json.loads(requests.request("GET", url, headers=headers).text)["response"]
# Remove all document in collection
leagues.delete_many({})
# Insert leagues in MongoDB database
result = leagues.insert_many(football_api_leagues)
pprint(result)

############################### Fixtures ###############################
# Get fixtures from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {"date":strftime("%Y-%m-%d")}
football_api_fixtures = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)["response"]
# Remove all document in collection
fixtures.delete_many({})
# Insert fixtures in MongoDB database
result = fixtures.insert_many(football_api_fixtures)
pprint(result)
