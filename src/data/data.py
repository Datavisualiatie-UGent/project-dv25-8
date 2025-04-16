import country_converter as coco
import diskcache
from datetime import datetime
from typing import Any
from procyclingstats import Ranking, Nation, Team, Teams, Rider
import sys

@diskcache.Cache('.cache/get_nations').memoize()
def get_nations(year: int) -> dict[str, Any]:
    try:
        ranking_nations = Ranking(f'statistics.php?season={year}&level=1&sekse=1&filter=Filter&p=nations')
        ranking_nations = ranking_nations.nations_ranking()
    except Exception as e:
        print(e)
        sys.exit()

    return [r.get('nation_url') for r in ranking_nations]

@diskcache.Cache('.cache/get_nation').memoize()
def get_nation(year: int, nation_url: str) -> dict[str, Any]:
    try:
        nation = Nation(year, nation_url)
    except Exception as e:
        print(e)
        sys.exit()

    nationality = coco.CountryConverter().convert(names=nation.name(), to='ISO2')
    nationality = nationality if nationality else None

    nation_ison = coco.CountryConverter().convert(names=nation.name(), to='ISOnumeric')
    nation_ison = nation_ison if nation_ison else None

    data = {}
    data['nation_name'] = nation.name()
    data['nationality'] = nationality
    data['nation_ison'] = nation_ison
    data['teams'] = nation.teams()
    data['riders'] = nation.riders()
    data['wins'] = nation.wins()
    data['pcs_points'] = nation.pcs_points()

    return data

@diskcache.Cache('.cache/get_teams').memoize()
def get_teams(year: int) -> list[str]:
    return Teams().teams(year)

@diskcache.Cache('.cache/get_team').memoize()
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
def get_riders(year: int) -> list[str]:
    return [rider_url for team_url in get_teams(year) for rider_url in get_team(team_url)['riders']]

@diskcache.Cache('.cache/get_rider').memoize()
def get_rider(year:int, rider_url: str) -> dict[str, Any]:
    try:
        rider = Rider(f'{rider_url}/{year}')
    except Exception as e:
        print(e)
        sys.exit()

    data = {}
    data['name'] = rider.name()
    data['nationality'] = rider.nationality()
    data['birthdate'] = rider.birthdate()
    data['age'] = year - datetime.strptime(data['birthdate'], '%Y-%m-%d').year
    data['place_of_birth'] = rider.place_of_birth()
    data['weight'] = rider.weight()
    data['height'] = rider.height()
    data['image_url'] = rider.image_url()
    data['teams_history'] = {str(d.get('season')): d.get('team_url') for d in rider.teams_history() if d.get('season') is not None}
    pcs_results = rider.points_per_season_history()
    data['pcs_points'] = {str(d['season']): d['points'] for d in pcs_results}
    data['pcs_ranks'] = {str(d['season']): d['rank'] for d in pcs_results}
    return data

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
