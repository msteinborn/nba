from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

GreenTabRap = [];
GreenTabYr = [];

BrownTabRap = [];
BrownTabYr = [];

data = np.genfromtxt('modern_RAPTOR_by_player.csv',dtype=('U15','U15','f','f','f','f','f','f','f','f','f','f','f','f','f'),delimiter=',' , names = [ 'player_name','player_id',
																		'season','poss','mp','raptor_offense',
																		'raptor_defense','raptor_total',
																		'war_total','war_reg_season',
																		'war_playoffs','predator_offense',
																		'predator_defense',
																		'predator_total','pace_impact'])



print(data['season'])
print(data['player_name'])

for i in range(0, len(data['player_name'])-1):
	if data['player_name'][i] == 'Stephen Curry':
		GreenTabRap.append(data['raptor_total'][i])
		GreenTabYr.append(data['season'][i])
		
	elif data['player_name'][i] == 'James Harden':
		BrownTabRap.append(data['raptor_total'][i])
		BrownTabYr.append(data['season'][i])



		
plt.scatter(GreenTabYr,GreenTabRap, label='Steph Curry')
plt.scatter(BrownTabYr, BrownTabRap,label='James Harden')
leg = plt.legend(fancybox = True);
plt.title("WAR James Harden vs Steph Curry")
plt.xlabel('Year')
plt.ylabel('WAR')
plt.show()