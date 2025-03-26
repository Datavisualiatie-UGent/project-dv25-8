import json
import sys
import logging
import country_converter as coco
from procyclingstats import Ranking

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize a dictionary to store results
data = {}

# Initialize the country converter (maps country names to ISO3 codes)
cc = coco.CountryConverter()

nations = {'ranking': {}, 'riders': {}}

# Extract the number of World tour riders per country over the years
for year in range(1930, 2026):
    ranking = Ranking(f"statistics.php?season={year}&level=1&sekse=1&filter=Filter&p=nations")
    ranking = ranking.statistics_ranking('nation_name', 'rank', 'number_riders')

    # Convert nation names to ISO3 codes
    for nation in ranking:
        nation_name = nation['nation_name']
        iso3 = cc.convert(names=nation_name, to='ISOnumeric')  # Convert the nation name to ISO3 code
        nation['country_iso3'] = iso3 if iso3 else None

    nations['ranking'][f'{year}'] = ranking

    # Get all the riders in that year for the different nations
    nations['riders'][f'{year}'] = {}
    for nation in ranking:
        conversion_country = cc.convert(names=nation['nation_name'], to='ISO2')

        if conversion_country == 'not found':
            # Set the country to the full name
            conversion_country = nation['nation_name']

        riders = Ranking(f"nation.php?season={year}&level=wt&filter=Filter&id=" +
                         f"{conversion_country}&c=me&p=overview&s=contract-riders")
        riders = riders.individual_ranking('rider_name', 'team_name')

        nations['riders'][f'{year}'][f'{nation['country_iso3']}'] = riders


data['nations'] = nations

# Extract the average age of World tour riders over the years
ages = {'average': {}, 'youngest': {}}

for year in range(1930, 2026):
    ranking = Ranking(f"statistics.php?year={year}&level=1&sekse=1&filter=Filter&p=teams&s=average-age")
    ranking = ranking.statistics_ranking('rank', 'team_name', 'average_age')

    ages['average'][f'{year}'] = ranking

# Extract the youngest riders in the World tour over the years
for year in range(1980, 2026):
    ranking = Ranking(f"statistics.php?year={year}&sekse=1&level=1&filter=Filter&p=riders&s=youngest-riders")
    ranking = ranking.statistics_ranking('rank', 'rank', 'rider_name', 'min_age')

    ages['youngest'][f'{year}'] = ranking

data['ages'] = ages

# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))
