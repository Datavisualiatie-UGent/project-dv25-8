import json
import sys
import country_converter as coco
from procyclingstats import Ranking


# List with the names of the most important races
racelist = ['tour-de-france', 'giro-d-italia', 'vuelta-a-espana', 'paris-roubaix',
            'liege-bastogne-liege', 'milano-sanremo', 'ronde-van-vlaanderen',
            'il-lombardia', 'world-championship']

# Initialize a dictionary to store results
data = {'winners': {}}

# Initialize the country converter (maps country names to ISO3 codes)
cc = coco.CountryConverter()

for race in racelist:
    # Extract for every race the most winning riders
    ranking = Ranking(f'race.php?fnation=&stripped=0&filter=Filter&id1={race}&id2=results&id3=most-wins')
    ranking = ranking.individual_wins_ranking('rider_name', 'nationality', 'first_places', 'rank')

    # Convert nation names to ISO3 codes
    for rider in ranking:
        nationality = rider['nationality']
        iso3 = cc.convert(names=nationality, to='ISOnumeric')  # Convert the nation name to ISO3 code
        rider['nationality'] = iso3 if iso3 else None

    data['winners'][f'{race}'] = ranking


# Write the data as a JSON format to stdout
sys.stdout.buffer.write(json.dumps(data, indent=4).encode('utf-8'))
