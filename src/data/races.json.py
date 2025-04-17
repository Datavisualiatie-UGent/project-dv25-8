import json
import sys
import country_converter as coco
from data import get_wins_list_for_race, get_race_details


# List with the names of the most important races
racelist = ['tour-de-france', 'giro-d-italia', 'vuelta-a-espana', 'paris-roubaix',
            'liege-bastogne-liege', 'milano-sanremo', 'ronde-van-vlaanderen',
            'il-lombardia', 'world-championship']

# Initialize a dictionary to store results
data = {
    'winners': {},
    'raceInfo': {}
}

# Initialize the country converter (maps country names to ISO3 codes)
cc = coco.CountryConverter()

for race in racelist:
    # Extract for the given race the most winning riders
    data['winners'][f'{race}'] = get_wins_list_for_race(race)

    # Extract for the given race the distances and the average speed
    data['raceInfo'][f'{race}'] = get_race_details(race)

# Fix data errors:
# 1. The distance for the 1953 edition of Liege-Bastogne-Liege is incorrect (2 winners, so distance was double)
# 2. The distance for the 1949 edition of Paris-Roubaix is incorrect (2 winners, so distance was double)
data['raceInfo']['liege-bastogne-liege'][2025-1957]['distance'] = \
                                                    data['raceInfo']['liege-bastogne-liege'][2025-1957]['distance'] / 2
data['raceInfo']['paris-roubaix'][2025-1949]['distance'] = data['raceInfo']['paris-roubaix'][2025-1949]['distance'] / 2


# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))
