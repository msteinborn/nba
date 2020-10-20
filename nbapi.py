from nba_api.stats.endpoints import playercareerstats, playergamelog
import pandas as pd
import numpy as np
import datetime


# Myles Turner Bubble Stats
# career = playercareerstats.PlayerCareerStats(player_id='1626167')
# career = career.get_data_frames()[0]


domas_games =  playergamelog.PlayerGameLog(player_id="1627734", season = "ALL")
domas_games = domas_games.get_data_frames()[0]

myles_games = playergamelog.PlayerGameLog(player_id="1626167", season = "ALL")
myles_games = myles_games.get_data_frames()[0]





for i in myles_games.Game_ID:
    for j in domas_games.Game_ID:
        if (i == j):
            myles_games = myles_games[myles_games.Game_ID != i]


pacers_playoffs = playergamelog.PlayerGameLog(player_id="1626167", season = "ALL", season_type_all_star = "Playoffs")
pacers_playoffs = pacers_playoffs.get_data_frames()[0]


myles_games = pd.concat([pacers_playoffs,myles_games])

new_dates =[]
for i in myles_games.GAME_DATE:
    i = datetime.datetime.strptime(i, '%b %d, %Y')
    new_dates.append(i)
myles_games.GAME_DATE = new_dates

myles_games = myles_games[myles_games.GAME_DATE > datetime.datetime(2017,7,30)]









print(myles_games)
print("PTS:", round(myles_games.PTS.mean(),1), "REB: ",round(myles_games.REB.mean(),1), "AST: ", round(myles_games.AST.mean(),1),"plus minus:  ", myles_games.PLUS_MINUS.sum());


last_n_games = 0
