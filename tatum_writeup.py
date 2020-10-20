import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt


current_rap = pd.read_csv('latest_RAPTOR_by_player - Copy.csv')
current_rap["USG"] = ""
current_rap["TS"] = ""
current_rap["POS"] = ""
last_player = " "


adv_stats = pd.read_csv('players_adv20.csv')



for i in range(len(current_rap.player_name)):
    for j in range(len(adv_stats.Player)):
        if current_rap.player_name[i] == adv_stats.Player[j] and adv_stats.Player[j] != last_player:
            last_player = adv_stats.Player[j]
            current_rap.loc[i,'USG'] = float(adv_stats.USG[j])
            current_rap.loc[i,'TS'] = float(adv_stats.TS[j])
            current_rap.loc[i,'POS'] = adv_stats.Pos[j]

current_rap.drop(current_rap[current_rap.USG == ""].index, inplace=True)
current_rap.drop(current_rap[current_rap.TS == ""].index, inplace=True)
current_rap.drop(current_rap[current_rap.mp < 500].index, inplace=True)
current_rap.reset_index(drop=True,inplace=True)

print(current_rap[current_rap["player_name"] == "Jayson Tatum"])


## Im thinkinking WAR vs min played or USGessions

X_mean = current_rap.war_reg_season.mean()
X_sd = current_rap.war_reg_season.std()

current_rap['war_z'] = (current_rap.war_reg_season -X_mean)/X_sd

print(current_rap.war_z.max())

tatum_war_z, tatum_usg = current_rap[current_rap["player_name"] == "Jayson Tatum"]['war_z'].values[0], current_rap[current_rap["player_name"] == "Jayson Tatum"]['USG'].values[0]

print(tatum_war_z)
plot1 = plt.figure(1)
plt.style.use("fivethirtyeight")
plt.scatter(current_rap.war_z, current_rap.USG, alpha=0.8)




for i in range(len(current_rap.player_name)):
        if(current_rap.war_z[i] >= tatum_war_z and current_rap.USG[i] <= tatum_usg):
            plt.annotate(current_rap.player_name[i],                       # This the name of the top scoring player. Refer to the .head() from earlier
                     (current_rap.war_z[i] ,current_rap.USG[i]),                     # This is the point we want to annotate.
                     (current_rap.war_z[i], current_rap.USG[i]+.2),                    # These are coords for the text
                     arrowprops=dict(arrowstyle='-'),
                     c = '#a10b68' )    # Here we use a flat line for the arrow '-'
        elif(current_rap.war_z[i] >= tatum_war_z):
            plt.annotate(current_rap.player_name[i],                       # This the name of the top scoring player. Refer to the .head() from earlier
                     (current_rap.war_z[i] ,current_rap.USG[i]),                     # This is the point we want to annotate.
                     (current_rap.war_z[i], current_rap.USG[i]+.2),                    # These are coords for the text
                     arrowprops=dict(arrowstyle='-'),
                     c = '#da431a' )



current_rap.drop(current_rap[(current_rap.POS != "PF") & (current_rap.POS !="SF")].index, inplace=True)
current_rap.reset_index(drop=True,inplace=True)




plot2 = plt.figure(2)
plt.style.use("fivethirtyeight")
plt.scatter(current_rap.raptor_offense, current_rap.raptor_defense, alpha=0.8)
plt.axhline(0,color='red', alpha = 0.5) # x = 0
plt.axvline(0,color='red', alpha = 0.5) # y = 0



for i in range(len(current_rap.player_name)):
        if(current_rap.raptor_offense[i] >1.5 and current_rap.raptor_defense[i] >1.5):
            plt.annotate(current_rap.player_name[i],                       # This the name of the top scoring player. Refer to the .head() from earlier
                     (current_rap.raptor_offense[i] ,current_rap.raptor_defense[i]),                     # This is the point we want to annotate.
                     (current_rap.raptor_offense[i], current_rap.raptor_defense[i]+.2),                    # These are coords for the text
                     arrowprops=dict(arrowstyle='-'))    # Here we use a flat line for the arrow '-'

plt.show()
