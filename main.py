import argparse
import pandas as pd
import tensorflow as tf
from src.Predict import NN_Runner, XGBoost_Runner
from src.Utils.Dictionaries import team_index_current
from src.Utils.tools import get_json_data, to_data_frame, get_todays_games_json, create_todays_games, get_latest_file
import json
from src.Utils.odds_generation import generate_odds

todays_games_url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2022/scores/00_todays_scores.json'
data_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2022-23&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='


def createTodaysGames(games, df):
    match_data = []
    todays_games_uo = []
    home_team_odds = []
    away_team_odds = []

    input_json = json.load(open(get_latest_file('./Odds-Input')))
    # print(input_json)
    for game in games:
        home_team = game[0]
        away_team = game[1]

        json_obj = next((x for x in input_json if [team_index_current.get(x['id'][0]), team_index_current.get(
            x['id'][1])] == [team_index_current.get(home_team), team_index_current.get(away_team)]), None)

        # keep these for manual inputasdfas
        if input_json is None or json_obj is None:
            todays_games_uo.append(
                input(home_team + ' vs ' + away_team + ': '))
            home_team_odds.append(input(home_team + ' odds: '))
            away_team_odds.append(input(away_team + ' odds: '))
        else:
            todays_games_uo.append(str(json_obj['o/u']))
            home_team_odds.append(str(json_obj['home']))
            away_team_odds.append(str(json_obj['away']))

        home_team_series = df.iloc[team_index_current.get(home_team)]
        away_team_series = df.iloc[team_index_current.get(away_team)]
        stats = pd.concat([home_team_series, away_team_series])
        match_data.append(stats)

    games_data_frame = pd.concat(match_data, ignore_index=True, axis=1)
    games_data_frame = games_data_frame.T

    frame_ml = games_data_frame.drop(
        columns=['TEAM_ID', 'CFID', 'CFPARAMS', 'TEAM_NAME'])
    data = frame_ml.values
    data = data.astype(float)

    return data, todays_games_uo, frame_ml, home_team_odds, away_team_odds


def main():
    data = get_todays_games_json(todays_games_url)
    games = create_todays_games(data)
    data = get_json_data(data_url)
    df = to_data_frame(data)
    generate_odds()
    data, todays_games_uo, frame_ml, home_team_odds, away_team_odds = createTodaysGames(
        games, df)

    if args.nn:
        print("------------Neural Network Model Predictions-----------")
        data = tf.keras.utils.normalize(data, axis=1)
        NN_Runner.nn_runner(data, todays_games_uo, frame_ml,
                            games, home_team_odds, away_team_odds)
        print("-------------------------------------------------------")
    if args.xgb:
        print("---------------XGBoost Model Predictions---------------")
        XGBoost_Runner.xgb_runner(
            data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds)
        print("-------------------------------------------------------")
    if args.A:
        print("---------------XGBoost Model Predictions---------------")
        XGBoost_Runner.xgb_runner(
            data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds)
        print("-------------------------------------------------------")
        data = tf.keras.utils.normalize(data, axis=1)
        print("------------Neural Network Model Predictions-----------")
        NN_Runner.nn_runner(data, todays_games_uo, frame_ml,
                            games, home_team_odds, away_team_odds)
        print("-------------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model to Run')
    parser.add_argument('-xgb', action='store_true',
                        help='Run with XGBoost Model')
    parser.add_argument('-nn', action='store_true',
                        help='Run with Neural Network Model')
    parser.add_argument('-A', action='store_true', help='Run all Models')
    parser.add_argument('-init', action='store_true',
                        help='Generate Input JSON')
    args = parser.parse_args()
    main()
