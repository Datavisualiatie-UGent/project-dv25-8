import country_converter as coco
import diskcache
import sys
from datetime import datetime
from typing import Any
from procyclingstats import Ranking, Nation, Team, Teams, Rider


@diskcache.Cache('.cache/get_nations').memoize()
def get_nations(year: int) -> list[str, Any]:
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
    data['name'] = nation.name()
    data['nationality'] = nationality
    data['ison'] = nation_ison
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
    data['name'] = team.name()
    data['abbreviation'] = team.abbreviation()
    data['nationality'] = team.nationality()
    data['class'] = team.status()
    data['bike_brand'] = team.bike()
    data['season_wins'] = team.wins_count()
    data['pcs_points'] = team.pcs_points()
    data['pcs_rank'] = team.pcs_ranking_position()
    data['uci_rank'] = team.uci_ranking_position()
    data['riders'] = [rider.get('rider_url') for rider in team.riders('rider_url')]

    return data

@diskcache.Cache('.cache/get_riders').memoize()
def get_riders(year: int) -> list[str]:
    return [rider_url for nation_url in get_nations(year) for rider_url in get_nation(year, nation_url)['riders']]

@diskcache.Cache('.cache/get_rider').memoize()
def get_rider(rider_url: str) -> dict[str, Any]:
    try:
        rider = Rider(rider_url.strip())
    except Exception:
        return {}

    data = {}
    data['name'] = rider.name()
    data['nationality'] = rider.nationality()
    data['birthdate'] = rider.birthdate()
    data['place_of_birth'] = rider.place_of_birth()
    data['weight'] = rider.weight()
    data['height'] = rider.height()
    data['image_url'] = rider.image_url()
    data['teams_history'] = {str(d.get('season')): d.get('team_url') for d in rider.teams_history('season', 'team_url') if d.get('season') is not None}
    pcs_results = rider.points_per_season_history()
    data['pcs_points'] = {str(d['season']): d['points'] for d in pcs_results} if pcs_results is not [] else {}
    data['pcs_ranks'] = {str(d['season']): d['rank'] for d in pcs_results} if pcs_results is not [] else {}
    return data


@diskcache.Cache(".cache/get_wins_ranking_top3").memoize()
def get_wins_ranking_top3(year: int) -> list[dict[str, Any]]:
    # Get the wins ranking for the given year
    ranking = Ranking(f"statistics.php?year={year}&mw=1&filter=Filter&p=riders&s=wins-on-wt-level")
    ranking = ranking.statistics_ranking('rank', 'rider_name', 'number_of_wins', 'rider_url')
    converter = coco.CountryConverter()

    # Only use the top 3 riders for the ranking
    # Separate top 3 and rest
    top3 = ranking[:3]

    # Retreive the nationality and the picture for the top 3 riders
    for rider in top3:
        # Get the rider information
        rider_url = rider['rider_url']
        rider_data = Rider(rider_url)

        rider['picture'] = rider_data.image_url()

        # Conver the nationality from ISO2 to string
        rider['nationality'] = rider_data.nationality()
        rider['nationality'] = converter.convert(names=rider['nationality'], src="ISO2", to="name_short")

    return top3

@diskcache.Cache(".cache/get_wins_ranking").memoize()
def get_wins_ranking(year: int) -> list[dict[str, Any]]:
    # Get the wins ranking for the given year
    ranking = Ranking(f"statistics.php?year={year}&mw=1&filter=Filter&p=riders&s=wins-on-wt-level")
    ranking = ranking.statistics_ranking('rank', 'rider_name', 'number_of_wins', 'rider_url')

    # Build lookup dictionary
    def swap_name(full_name: str) -> str:
        parts = full_name.split()
        for i, part in enumerate(parts):
            if not part.isupper():
                # Assume first name starts here
                last_name = " ".join(parts[:i+1])
                first_name = " ".join(parts[i+1:])
                return f"{last_name} {first_name}".upper()
        return ""  # fallback if nothing is all caps

    lookup = {swap_name(r["rider_name"]): r["number_of_wins"] for r in ranking}
    return lookup


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
    ranking_fastest = Ranking(f'race/{race}/results/fastest-editions')
    ranking_fastest = ranking_fastest.statistics_ranking('year', 'distance', 'average_speed')

    ranking_dropouts = Ranking(f'race/{race}/results/dropouts-per-edition')
    ranking_dropouts = ranking_dropouts.statistics_ranking('year', 'participants', 'dropouts')

    # Convert to dictionaries keyed by year
    fastest_by_year = {entry['year']: entry for entry in ranking_fastest}
    dropouts_by_year = {entry['year']: entry for entry in ranking_dropouts}

    # Combine all unique years
    all_years = sorted(set(fastest_by_year) | set(dropouts_by_year))

    # Join data
    merged = []
    for year in all_years:
        merged_entry = {'year': year}
        merged_entry.update(fastest_by_year.get(year, {}))
        merged_entry.update(dropouts_by_year.get(year, {}))
        merged.append(merged_entry)

    return merged

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
    ranking = ranking.statistics_ranking('team_name', 'team_url', 'number_of_wins')

    return ranking


if __name__ == '__main__':
    pass
