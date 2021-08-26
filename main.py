from pymongo import MongoClient
from pprint import pprint
from time import strftime
import requests
import json
from termcolor import colored

with open('conf/conf.json') as f:
    conf = json.load(f)

# MongoDb configuration
client = MongoClient("{}:{}".format(conf["host"], conf["port"]))
db=client[conf["db"]]
countries_col = db["Countries"] # Countries collection
leagues_col = db["Leagues"] # Leagues collection
fixtures_col = db["Fixtures"] # Fixtures collection

with open('conf/key.json') as f:
    key = json.load(f)

# Rapid API account configuration
headers = {
    'x-rapidapi-key': key["key"],
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

# Countries list
countries = ["France", "Italy", "Portugal", "Belgium", "Spain", "England", "Germany", "World"]

############################### Countries ###############################
# Remove all documents in collection
countries_col.delete_many({})
# Get countries from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/countries"
football_api_countries = json.loads(requests.request("GET", url, headers=headers).text)
# Filter countries
football_api_countries = [country for country in football_api_countries["response"] if country["name"] in countries]
# Insert countries in MongoDB database
result = countries_col.insert_many(football_api_countries)
if result : print(colored('Countries successfully inserted', 'green'))
else : print(colored('Error : countries insertion failed', 'red'))

############################### Leagues ###############################
# Remove all documents in collection
leagues_col.delete_many({})
# Get leagues from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
for country in countries:
    querystring = {"country": country}
    football_api_leagues = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
    # Insert leagues in MongoDB database
    result = leagues_col.insert_many(football_api_leagues["response"])
    if result : print(colored(f'{country} leagues successfully inserted', 'green')) 
    else : print(colored(f'Error : {country} leagues insertion failed'), 'red')

############################### Fixtures ###############################
# Get fixtures from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {"date":strftime("%Y-%m-%d")}
football_api_fixtures = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
# Remove all documents in collection
fixtures_col.delete_many({})
# Insert fixtures in MongoDB database
result = fixtures_col.insert_one(football_api_fixtures)
pprint(result)
