import json
import sys
import logging
from data import get_equipment_for_teams, get_number_of_wins_for_teams

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize a dictionary to store results
data = {
    'teamsInfo': [],
}

# extract the equipment of the teams over the years
for year in range(2010, 2026):
    logger.info(year)
    equipment_teams = get_equipment_for_teams(year)
    wins_teams = get_number_of_wins_for_teams(year)

    # Create a dictionary to store equipment by team name
    equipment_dict = {team['team_name'].strip(): team for team in equipment_teams}

    # Iterate through wins_teams and combine with equipment data
    for team in wins_teams:
        team_name = team['team_name'].strip()
        if team_name in equipment_dict:
            equipment_data = equipment_dict[team_name]
            # Create a new dictionary combining equipment and wins
            combined_data = {
                'team_name': team_name,
                'bike': equipment_data['bike'],
                'groupset': equipment_data['groupset'],
                'wheels': equipment_data['wheels'],
                'wins': team.get('number_of_wins', 0)
            }
            data['teamsInfo'].append(combined_data)

# data['equipment'] = equipment
# data['wins'] = wins

# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))
