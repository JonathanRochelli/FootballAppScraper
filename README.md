# Football APP API Scraper

The main objective of the repository is to set up a development architecture for the API [football-api](https://rapidapi.com/api-sports/api/api-football) available on [Rapid API](https://rapidapi.com/). This architecture allows us to copy the data available on the API in a local database. So, you can use the API without pay. Only by using the Basic Plan. The data need to be updated by yourself, but in a development architecture the data do not need to be updated in real-time.

## Collect

This repository allows to collect the data from the API available on the website [Rapid API](https://rapidapi.com/api-sports/api/api-football)
The API football-api contains +860 football leagues&cups. Livescore (15s), odds, events, line-ups, coachs, players, top scorers, standings, statistics, transfers, predictions.

Documentation : [API-FOOTBALL API Documentation](https://www.api-football.com/documentation-v3)

## Python script

The Python script allows us to collect the data from the API and save them in MongoDB database. You can use the Basic plan on Rapid api.
The data are available in unlimited amounts because they are saved in a local database. So the data are available without subscription.
**The usage is unlimited!!**

## Install dependencies

```
pip install -r requirements.txt
```

## How to use?

1. You need to create an account on [Rapid API](https://rapidapi.com/)
2. Subscribe to the API [football-api](https://rapidapi.com/api-sports/api/api-football)
3. Add the Rapid API key in a file ./key.txt
4. Set up MongoDB database on **localhost:27017**
5. Create the collections (Countries, Leagues)
6. Activate the virtual environment ( [Python3 Venv Documentation](https://docs.python.org/fr/3/library/venv.html) )
7. Install the dependencies
8. Run the application
'''
python3 main.py
'''
8. Enjoy!
