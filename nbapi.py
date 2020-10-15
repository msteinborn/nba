from nba_api.stats.endpoints import playercareerstats
import pandas
# Anthony Davis
career = playercareerstats.PlayerCareerStats(player_id='203076')
career = career.get_data_frames()[0]

print(career);
