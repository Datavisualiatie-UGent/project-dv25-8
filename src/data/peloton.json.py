import json
import sys
import logging
from data import *

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# What fi we do a map of riders, and keep active years, same for nation
data = {
    'nations': {}, # data['nations']['year']['nation_name'] = {}
    'riders': {}, # data['riders']['year']['nation_name']['rider_name'] = {}
    'ages': {
        'average': {},
        'youngest': {}
    }
}

for year in range(1930, 2026):
    nations = get_nations(year)
    data['nations'][f'{year}'] = nations

    data['riders'][f'{year}'] = {}
    for nation in nations:
        riders = get_riders(year, nation['nation_name'])
        data['nations'][f'{year}'][nation['nation_name']]['number_of_riders'] = len(riders.keys())
        data['riders'][f'{year}'][f'{nation['nation_name']}'] = riders

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
