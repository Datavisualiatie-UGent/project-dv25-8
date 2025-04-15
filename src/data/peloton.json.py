import json
import sys
import logging
from data import get_nations_ranking, get_riders, get_riders_2, get_wins_ranking

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize a dictionary to store results
data = {
    'nations': {
        'ranking': {},
        'riders': {},
        'riders2': {}
    },
    'wins': {
        'ranking': {},
    }
}

# Extract the number of World tour riders per country over the years
for year in range(1930, 2026):
    nations_ranking = get_nations_ranking(year)
    data['nations']['ranking'][f'{year}'] = nations_ranking

    data['nations']['riders'][f'{year}'] = {}
    data['nations']['riders2'][f'{year}'] = {}
    for nation in nations_ranking:
        nation_name = nation['nation_name']
        nation_iso3 = nation['nation_iso3']
        riders = get_riders(year, nation_name)
        data['nations']['riders'][f'{year}'][f'{nation_iso3}'] = riders
        data['nations']['riders2'][f'{year}'][f'{nation_iso3}'] = get_riders_2(year, nation_name)

    wins_ranking = get_wins_ranking(year)
    data['wins']['ranking'][f'{year}'] = wins_ranking


# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))
