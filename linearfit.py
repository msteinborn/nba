import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt

# Here we access the leagueleaders module through endpoints & assign the class to "data"
data = endpoints.leagueleaders.LeagueLeaders(season="2019-20",  	season_type_all_star= "Regular Season")

# Our "data" variable now has built in functions such as creating a dataframe for our data
df = data.league_leaders.get_data_frame()

df = df.drop(df[df.FGA < 450].index)
df = df.drop(df[df.PTS/df.GP < 10].index)
df = df.reset_index(drop=True)


print(df.head())


##Begin to create linear_model

x, y = df.FG_PCT, df.EFF
##Reshape array from 1d to 2d

x=np.array(x).reshape(-1,1)
y=np.array(y).reshape(-1,1)


print(x[0:5],y[0:5])

# create a lneear model and then fit it to dataset

model = linear_model.LinearRegression()
model.fit(x,y)

## find r2

r2 = round(model.score(x,y), 2)
predicted_y = model.predict(x)


plt.scatter(x, y, s=15, alpha=.5)                            # Scatterplot:  Specfiy size(s) and transparency(alpha) of dots
plt.plot(x, predicted_y, color = 'black')                    # line: Add line for regression line w/ predicted values
plt.title('NBA - Relationship Between FGA and PPG')          # Give it a title
plt.xlabel('FG3PCT')                                   # Label x-axis
plt.ylabel('EFF Per Game')                                # Label y-axis
plt.text(0.4,1500, f'R2={r2}')                                  # 10, 25 are the coordinates for our text. Adjust accordingly


for i in range(len(df.PLAYER)):
    if(df.PTS[i]/df.GP[i] > 20):
        plt.annotate(df.PLAYER[i],                       # This the name of the top scoring player. Refer to the .head() from earlier
                     (x[i], y[i]),                       # This is the point we want to annotate.
                     (x[i]-.01,y[i]-.02),                    # These are coords for the text
                     arrowprops=dict(arrowstyle='-'))    # Here we use a flat line for the arrow '-'


plt.show()
