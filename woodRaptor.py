import pandas as pd
from matplotlib import pyplot as plt


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
                                'Andre Drummond'
]]

centers = centers.loc[:, ['mp', 'poss', 'war_reg_season', 'raptor_total']]

ax1 = centers.plot.scatter(x='poss',

                      y='raptor_total',

                      c='DarkBlue')

for k, v in centers.loc[:,['poss', 'raptor_total']].iterrows():
    ax1.annotate(k, v)

ax2 = centers.plot.scatter(x ='raptor_total',
                           y='war_reg_season')

for k, v in centers.loc[:,['raptor_total', 'war_reg_season']].iterrows():
                               ax2.annotate(k, v)




plt.show()
