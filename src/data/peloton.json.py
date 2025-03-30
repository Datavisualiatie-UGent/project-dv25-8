import json
import sys
import logging
from data import *

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
    'ages': {
        'average': {},
        'youngest': {}
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

# Extract the average age of World tour riders over the years
for year in range(1930, 2026):
    ranking = get_average_age(year)
    data['ages']['average'][f'{year}'] = ranking

# Extract the youngest riders in the World tour over the years
for year in range(1980, 2026):
    ranking = get_youngest_age(year)
    data['ages']['youngest'][f'{year}'] = ranking

# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))
