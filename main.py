from pymongo import MongoClient
from pprint import pprint
from time import strftime
import requests
import json
from termcolor import colored
import pendulum

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

request = 0

# Countries list
countries_selected = ["France", "Italy", "Portugal", "Belgium", "Spain", "England", "Germany", "World"]
leagues_selected = [61, 71, 94, 140, 39, 78, 2, 3, 1, 4]

############################### Countries ###############################
# Remove all documents in collection
countries_col.delete_many({})
# Get countries from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/countries"
football_api_countries = json.loads(requests.request("GET", url, headers=headers).text)
# Filter countries
football_api_countries = [country for country in football_api_countries["response"] if country["name"] in countries_selected]
# Insert countries in MongoDB database
result = countries_col.insert_many(football_api_countries)
# Print result
if result : print(colored('Countries successfully inserted', 'green'))
else : print(colored('Error : Countries insertion failed', 'red'))
request += 1

############################### Leagues ###############################
# Remove all documents in collection
leagues_col.delete_many({})
# Get leagues from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
football_api_leagues = json.loads(requests.request("GET", url, headers=headers).text)
request += 1
for country in countries_selected:
    # Filter leagues by country
    leagues = [l for l in football_api_leagues["response"] if l["country"]["name"] == country]
    # Insert leagues in MongoDB database
    result = leagues_col.insert_many(leagues)
    # Print result
    if result : print(colored(f'{country} leagues successfully inserted', 'green')) 
    else : print(colored(f'Error : {country} leagues insertion failed'), 'red')

############################### Fixtures ###############################
# Remove all documents in collection
fixtures_col.delete_many({})
# Find next sunday
next_sunday = pendulum.now().next(pendulum.SUNDAY).strftime('%Y-%m-%d')
# Get fixtures from football-api
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {"date":next_sunday, "season" : 2021}
football_api_fixtures = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
request += 1
# Filter fixtures by league
fixtures = [f for f in football_api_fixtures["response"] if f["league"]["id"] in leagues_selected and f["league"]["country"] in countries_selected]
# Insert fixtures in MongoDB database
result = fixtures_col.insert_many(fixtures)
if result : print(colored(f'{next_sunday} - Fixtures successfully inserted', 'green')) 
else : print(colored(f'Error : {next_sunday} - Fixtures insertion failed'), 'red')

print(f'{request} requests was executed')
