import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt

# Here we access the leagueleaders module through endpoints & assign the class to "data"
data = endpoints.leaguedashplayerstats.LeagueDashPlayerStats(season="2019-20",  	season_type_all_star= "Playoffs")

## Get salaries from BBALL-reference data
salaries = pd.read_csv('salary.csv')


# Our "data" variable now has built in functions such as creating a dataframe for our data
df= data.league_dash_player_stats.get_data_frame()

fp = df.NBA_FANTASY_PTS;



##Create new datafram with information we actually want
fantasy=pd.DataFrame(list(zip(fp,df.PLAYER_NAME,df.GP)), columns = ['score','PLAYER_NAME','GP'])

fantasy = fantasy.sort_values(by='score',ascending = False)
##Create a new column and fill its values with NaN
fantasy["contract"] = np.nan;

## For loop to fill contract data into our data frame
for i in range(len(fantasy.PLAYER_NAME)):
    for j in range(len(salaries.Player)):
        if fantasy.PLAYER_NAME[i] == salaries.Player[j]:
            fantasy.loc[i,'contract'] = ((salaries.loc[j,'2019-20']))

## sorting array and setting indexes
fantasy = fantasy.set_index(fantasy.PLAYER_NAME)
fantasy = fantasy.drop(columns = "PLAYER_NAME")

##drop values that make player invalid (<5games and <100 fantasy points)
fantasy.drop(fantasy[fantasy.score < 100].index, inplace=True)
fantasy.drop(fantasy[fantasy.GP <= 5].index, inplace=True)


## find each players fantasy poitns added per game
fantasy["fpg"] =round((fantasy.score/fantasy.GP),1)

## find the mean of Fantasy Points/per game
meanfpg = fantasy['fpg'].mean()

## find standard deviation
fantasy["fpgsd"] = round((fantasy.fpg**2 - meanfpg**2),2)
sdfpg= np.sqrt(fantasy['fpgsd'].mean())

## variance of points versus
fantasy["variance"]= round((fantasy.fpg**2-meanfpg**2)/(sdfpg**2),3)
fantasy["value"] =  round(np.sign(fantasy.variance)*(fantasy.variance**2)*1000000/fantasy.contract,2);

fantasy = fantasy.sort_values(by='value',ascending = False)
fantasy = fantasy.dropna()



##Plotting of values begins here
plt.rcParams["figure.figsize"] = (20,10)
x,y = (fantasy.contract[0:100]/1000000),fantasy.variance[0:100]

x=np.array(x).reshape(-1,1)
y=np.array(y).reshape(-1,1)


# create a lneear model and then fit it to dataset

model = linear_model.LinearRegression()
model.fit(x,y)

## find r2

r2 = round(model.score(x,y), 2)
predicted_y = model.predict(x)



print(fantasy[:])
print( "::: median FP/G", meanfpg, "vsdfpg", round(sdfpg,3))

plt.scatter(x, y, s=15, alpha=1, color= "#333333")                            # Scatterplot:  Specfiy size(s) and transparency(alpha) of dots
plt.plot(x, predicted_y, color = 'black')
plt.text(20,7, f'R2={r2}')
plt.title('NBA - Relationship Between Fantasy Points Added and Contract Values')          # Give it a title
plt.xlabel('Contract Value')                                   # Label x-axis
plt.ylabel('Variation from mean Fantasy Points per Game')

for i in range(15):
        plt.annotate(fantasy.index[i],                       # This the name of the top scoring player. Refer to the .head() from earlier
                     (x[i], y[i]),                       # This is the point we want to annotate.
                     (x[i]+0.6,y[i]+.5),                    # These are coords for the text
                     arrowprops=dict(arrowstyle='-'))    # Here we use a flat line for the arrow '-'


        plt.annotate(i+1,                       # This the name of the top scoring player. Refer to the .head() from earlier
                      (x[i], y[i]),                       # This is the point we want to annotate.
                      (x[i],y[i]+.5),                    # These are coords for the text
                      color = '#8357ad')    # Here we use a flat line for the arrow '-'


plt.savefig('books_read.png')
fantasy.to_csv(index=False)
