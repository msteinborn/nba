import pandas as pd


# Reading CSV to get Raptor values for current nba

currentRap = pd.read_csv("latest_RAPTOR_by_player.csv")


currentRap.set_index('player_name', inplace=True)

#print(currentRap.head());

celtic_data = currentRap.loc[[
                              'Kemba Walker',
                              'Gordon Hayward',
                              'Jaylen Brown',
                              'Jayson Tatum',
                              'Daniel Theis' ]]

print(celtic_data)

celtic_war = celtic_data.loc[:,"war_reg_season"]

print(celtic_war.head())

print(celtic_war.sum())
