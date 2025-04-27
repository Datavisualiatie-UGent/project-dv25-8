import json
import sys
import logging
from data import *

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

data = {
    'nations': {},
    'teams': {},
    'riders': {},
    'wins': {
        'top3': {},
        'all': {}
    }
}

for year in range(1930, 2026):
    logger.info(year)
    # data['nations'][<year>][<name>] = {...}
    data['nations'][str(year)] = {}
    for nation_url in get_nations(year):
        nation = get_nation(year, nation_url)
        data['nations'][str(year)][nation['name']] = nation

    # data['teams'][<year>][<name>] = {...}
    data['teams'][str(year)] = {}
    for team_url in get_teams(year):
        team = get_team(team_url)
        data['teams'][str(year)][team['name']] = team

    # data['riders'][<year>][<name>] = {...}
    data['riders'][str(year)] = {}
    for rider_url in get_riders(year):
        rider = get_rider(rider_url)
        data['riders'][str(year)][rider['name']] = rider

    wins_ranking_top3 = get_wins_ranking_top3(year)
    data['wins']['top3'][f'{year}'] = wins_ranking_top3

    wins_ranking = get_wins_ranking(year)
    data['wins']['all'][f'{year}'] = wins_ranking

# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))

# Write to a file as backup
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
