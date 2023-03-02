from src.Utils.tools import get_odds
import json
from datetime import datetime
from dateutil import parser, tz

# api_key = 
url = 'https://api.the-odds-api.com/v4/sports/basketball_nba/odds/'\
    '?apiKey=2db533701475e3191e96b9f9115053aa&regions=us&markets=h2h,totals'\
        '&oddsFormat=american&bookmakers=fanduel'

def over_under_null(obj):
    if obj is None:
        return 999
    return obj['outcomes'][0]['point']

def generate_odds():
    games = get_odds(url)
    output = []
    for game in games:
        date = parser.parse(game['commence_time']).astimezone(tz.gettz('America/New_York'))

        fanduel = next((x for x in game['bookmakers'] if x['key'] == 'fanduel'), None)
        if fanduel is not None:
            fanduel_h2h = next((x for x in fanduel['markets'] if x['key'] == 'h2h'), None)
            fanduel_total = next((x for x in fanduel['markets'] if x['key'] == 'totals'), None)

            output.append(
                {
                    'date' : date.strftime('%m/%d/%Y'),
                    'id': [game['home_team'], game['away_team']],
                    'home':  next((x for x in fanduel_h2h['outcomes'] if x['name'] == game['home_team']), None)['price'],
                    'away':  next((x for x in fanduel_h2h['outcomes'] if x['name'] == game['away_team']), None)['price'],
                    'o/u': over_under_null(fanduel_total)
                }
            )            
    with open('./Odds-Input/odds-input-'+ datetime.today().strftime('%Y-%m-%d') + '.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

def main():
   generate_odds()

if __name__ == '__main__':
    main()