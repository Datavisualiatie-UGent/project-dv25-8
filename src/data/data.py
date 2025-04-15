import country_converter as coco
import diskcache
from datetime import datetime
from typing import Any
from procyclingstats import Ranking, Rider, Team, Teams
import sys

def get_nations(year: int) -> dict[str, Any]:
    try:
        ranking_nations = Ranking(f'statistics.php?season={year}&level=1&sekse=1&filter=Filter&p=nations')
        ranking_nations = ranking_nations.nations_ranking()
    except Exception as e:
        print(e)
        sys.exit()

    nations = {}
    for r in ranking_nations:
        key = r.get('nationality')
        nations[key] = {}

        nation_iso3 = coco.CountryConverter().convert(names=r.get('nation_name'), to='ISOnumeric')
        nation_iso3 = nation_iso3 if nation_iso3 else None

        nations[key]['nation_name'] = r.get('nation_name')
        nations[key]['nationality'] = r.get('nationality')
        nations[key]['nation_iso3'] = nation_iso3
        nations[key]['rank'] = r.get('rank')
        nations[key]['number_of_riders'] = r.get('number_riders')

    return nations

def get_teams(year: int) -> list[str]:
    return Teams().teams(year)

def get_team(team_url: str) -> dict[str, Any]:
    try:
        team = Team(team_url)
    except Exception as e:
        print(e)
        sys.exit()

    data = {}
    data['team_name'] = team.name()
    data['team_abbreviation'] = team.abbreviation()
    data['nationality'] = team.nationality()
    data['class'] = team.status()
    data['bike_brand'] = team.bike()
    data['season_wins'] = team.wins_count()
    data['pcs_points'] = team.pcs_points()
    data['pcs_rank'] = team.pcs_ranking_position()
    data['uci_rank'] = team.uci_ranking_position()
    data['riders'] = [rider.get('rider_url') for rider in team.riders()]

    return data

@diskcache.Cache('.cache/get_riders').memoize()
def get_riders(year: int, nation_name: str) -> dict[str, Any]:
    def age(year: int, birthdate: str) -> int:
        if birthdate is None:
            return None
        isoBirthdate = '-'.join(f'{int(part):02d}' for part in rider_information.birthdate().split('-'))
        return year - datetime.fromisoformat(isoBirthdate).date().year
    
    # Convert the nation name to iso2 to use in the filter
    country_iso2 = coco.CountryConverter().convert(names=nation_name, to='ISO2')
    country_iso2 = country_iso2 if country_iso2 != 'not found' else nation_name

    # Get the ranking of riders
    try:
        rankings = Ranking(f"nation.php?season={year}&level=wt&filter=Filter&id={country_iso2}&c=me&p=overview&s=contract-riders")
        individual_rankings = rankings.individual_ranking()
    except ValueError as e:
        print(e)
        return {}
    
    riders = {}
    for individual_ranking in individual_rankings:
        # Get rider information
        try:
            rider_information = Rider(f'{individual_ranking.get('rider_url')}/{year}')
        except:
            continue

        # Merge all available data
        riders[individual_ranking.get('rider_name')] = {
            'rider_name': individual_ranking.get('rider_name'),
            'rider_url': individual_ranking.get('rider_url'),
            'team_name': individual_ranking.get('team_name'),
            'team_url': individual_ranking.get('team_url'),
            'rank': individual_ranking.get('rank'),
            'previous_rank': individual_ranking.get('prev_rank'),
            'nationality': individual_ranking.get('nationality'),
            'points': individual_ranking.get('points'),
            'birthdate': rider_information.birthdate(),
            'age': age(year, rider_information.birthdate()),
            'weight': rider_information.weight(),
            'height': rider_information.height()
        }

    # Return the rider information
    return riders

@diskcache.Cache(".cache/get_average_age").memoize()
def get_average_age(year: int) -> list[dict[str, Any]]:
    ranking = Ranking(f"statistics.php?year={year}&level=1&sekse=1&filter=Filter&p=teams&s=average-age")
    ranking = ranking.statistics_ranking('rank', 'team_name', 'average_age')
    return ranking

@diskcache.Cache(".cache/get_youngest_age").memoize()
def get_youngest_age(year: int) -> list[dict[str, Any]]:
    ranking = Ranking(f"statistics.php?year={year}&sekse=1&level=1&filter=Filter&p=riders&s=youngest-riders")
    ranking = ranking.statistics_ranking('rank', 'rank', 'rider_name', 'min_age')
    return ranking

if __name__ == '__main__':
    pass
