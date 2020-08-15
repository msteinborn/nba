import pandas as pd
from matplotlib import pyplot as plt
from nba_api.stats.static import players
from nba_api.stats import endpoints



# Reading CSV to get Raptor values for current nba
currentRap = pd.read_csv("latest_RAPTOR_by_player.csv")


currentRap.set_index('player_name', inplace=True)

centers = currentRap.loc[[
                                'Christian Wood',
                                'Daniel Theis',
                                'Montrezl Harrell',
                                'Nikola Jokic',
                                'Joel Embiid',
                                'Clint Capela',
                                'Steven Adams',
                                'Andre Drummond',
                                'Hassan Whiteside',
                                'Jarrett Allen',
                                'Rudy Gobert'
]]

centers = centers.loc[:, ['mp', 'poss', 'raptor_offense', 'raptor_defense', 'raptor_total']]

ax1 = centers.plot.scatter(x='poss',

                      y='raptor_total',

                      c='DarkBlue')

for k, v in centers.loc[:,['poss', 'raptor_total']].iterrows():
    ax1.annotate(k, v)

ax2 = centers.plot.scatter(x ='raptor_defense',
                           y='raptor_offense')

for k, v in centers.loc[:,['raptor_defense', 'raptor_offense']].iterrows():
                               ax2.annotate(k, v)


ax2.vlines(0,-10,10,colors='red')
ax2.hlines(0,-10,10,colors='red')
ax2.set_xlim(-1,8)
ax2.set_ylim(-3,6)
ax2.grid()

#plt.show()
active_players = [i['id'] for i in players.get_active_players()]
stats = []

for i in range(len(active_players)):
    plyrs = endpoints.playerprofilev2.PlayerProfileV2(player_id=active_players[i])
    plyrs = plyrs.season_totals_regular_season.get_data_frame()
    stats.append(plyrs[-1:])

print(stats)
