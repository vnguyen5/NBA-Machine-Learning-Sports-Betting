import requests
import pandas as pd
from colorama import Style
import glob
import os
from datetime import datetime
import json as JSON
games_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en',
    'origin': 'http://stats.nba.com',
    'Referer': 'https://github.com'
}

data_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1&Season=2019-20&SeasonType=Regular%20Season',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}

def get_odds(url):
    raw_data = requests.get(url)
    return raw_data.json()


def get_json_data(url):
    raw_data = requests.get(url, headers=data_headers)
    json = raw_data.json()
    # with open('./cock-'+ datetime.today().strftime('%Y-%m-%d') + '.json', 'w', encoding='utf-8') as f:
    #     JSON.dump(json, f, ensure_ascii=False, indent=4)
    # input('asdf')
    return json.get('resultSets')


def get_todays_games_json(url):
    raw_data = requests.get(url, headers=games_header)
    json = raw_data.json()
    return json.get('gs').get('g')


def to_data_frame(data):
    data_list = data[0]
    return pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))


def create_todays_games(input_list):
    games = []
    for game in input_list:
        home = game.get('h')
        away = game.get('v')
        home_team = home.get('tc') + ' ' + home.get('tn')
        away_team = away.get('tc') + ' ' + away.get('tn')
        games.append([home_team, away_team])
    return games

def create_json_input(games):
    output = []
    for game in games:
        output.append(
            {
                'id': game,
                'home': '100',
                'away': '100',
                'o/u': '200'
            }
        )
    with open('./Odds-Input/odds-input-'+ datetime.today().strftime('%Y-%m-%d') + '.json', 'w', encoding='utf-8') as f:
        JSON.dump(output, f, ensure_ascii=False, indent=4)

def get_latest_file(path):
    list_of_files = glob.glob(f'{path}/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return(latest_file)

def team_print(team, ml):
    if int(ml) > 0:
        return team + Style.RESET_ALL + '(+' + str(ml) + ')'
    else:
        return team + Style.RESET_ALL + '(' + str(ml) + ')'