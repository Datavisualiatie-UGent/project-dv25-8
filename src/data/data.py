import country_converter as coco
import diskcache
from datetime import datetime
from typing import Any
from procyclingstats import Ranking, Rider


@diskcache.Cache(".cache/get_nations_ranking").memoize()
def get_nations_ranking(year: int) -> list[dict[str, Any]]:
    # Get nations ranking
    ranking = Ranking(f"statistics.php?season={year}&level=1&sekse=1&filter=Filter&p=nations")
    ranking = ranking.statistics_ranking('nation_name', 'rank', 'number_riders')

    # Add nation ISO3 codes
    converter = coco.CountryConverter()
    for nation in ranking:
        iso3 = converter.convert(names=nation['nation_name'], to='ISOnumeric')
        nation['nation_iso3'] = iso3 if iso3 else None

    return ranking


@diskcache.Cache(".cache/get_riders").memoize()
def get_riders(year: int, nation_name: str) -> list[dict[str, Any]]:
    # Convert the country name to iso2 to use in the filter
    converter = coco.CountryConverter()
    country_iso2 = converter.convert(names=nation_name, to='ISO2')
    country_iso2 = country_iso2 if country_iso2 != 'not found' else nation_name

    # Get the riders
    riders = Ranking(f"nation.php?season={year}&level=wt&filter=Filter&id={country_iso2}&c=me&p=overview&s=contract-riders")
    riders = riders.individual_ranking('rider_name', 'team_name')

    return riders


@diskcache.Cache(".cache/get_riders_2").memoize()
def get_riders_2(year: int, nation_name: str) -> list[dict[str, Any]]:
    # Convert the country name to iso2 to use in the filter
    country_iso2 = coco.CountryConverter().convert(names=nation_name, to='ISO2')
    country_iso2 = country_iso2 if country_iso2 != 'not found' else nation_name

    # Get a list of rider names
    rider_urls = Ranking(f"nation.php?season={year}&level=wt&filter=Filter&id={country_iso2}&c=me&p=overview&s=contract-riders")
    rider_urls = [d['rider_url'] for d in rider_urls.individual_ranking('rider_url')]

    # Get a list of rider information
    riders = []
    for rider_url in rider_urls:
        try:
            # Get the rider information
            rider = Rider(f'{rider_url}')
        except ValueError:
            continue

        # Make sure that the birthdate is valid (some are unknown on procyclingstats)
        if rider.birthdate():
            birthdate = '-'.join(f'{int(part):02d}' for part in rider.birthdate().split('-'))
            birthdate = datetime.fromisoformat(birthdate).date()
            today = datetime.today().date()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            riders.append({
                'name': rider.name(),
                'age': age,
                'nationality': rider.nationality()
            })

    return riders


@diskcache.Cache(".cache/get_wins_list_for_race").memoize()
def get_wins_list_for_race(race: str) -> list[dict[str, Any]]:
    '''
    Returns the list with the riders winning the given race and the number of wins.
    '''
    # Extract for every race the most winning riders
    ranking = Ranking(f'race.php?fnation=&stripped=0&filter=Filter&id1={race}&id2=results&id3=most-wins')
    ranking = ranking.individual_wins_ranking('rider_name', 'nationality', 'first_places', 'rank')

    # Convert nation names to ISO3 codes
    cc = coco.CountryConverter()
    for rider in ranking:
        nationality = rider['nationality']
        iso3 = cc.convert(names=nationality, to='ISOnumeric')  # Convert the nation name to ISO3 code
        rider['nationality'] = iso3 if iso3 else None

    return ranking


@diskcache.Cache(".cache/get_race_details").memoize()
def get_race_details(race: str) -> list[dict[str, Any]]:
    '''
    Returns the race details for all the years:
        - Distance
        - Average Speed
    '''
    ranking = Ranking(f'race/{race}/results/fastest-editions')
    ranking = ranking.statistics_ranking('year', 'distance', 'average_speed')

    return ranking


@diskcache.Cache(".cache/get_equipment_for_teams").memoize()
def get_equipment_for_teams(year: int) -> list[dict[str, Any]]:
    '''
    Returns the equipment used by the team for the given year.
    '''
    ranking = Ranking(f'statistics.php?season={year}&level=wt&filter=Filter&p=gear')
    ranking = ranking.statistics_ranking('team_name', 'bike', 'groupset', 'wheels')

    return ranking


@diskcache.Cache(".cache/get_number_of_wins_for_teams").memoize()
def get_number_of_wins_for_teams(year: int) -> list[dict[str, Any]]:
    '''
    Returns the number of wins for the teams for the given year.
    '''
    ranking = Ranking(f'statistics.php?year={year}&filter=Filter&p=teams&s=wt-wins-for-wt-teams')
    ranking = ranking.statistics_ranking('team_name', 'number_of_wins')

    return ranking
