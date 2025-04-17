import country_converter as coco
import diskcache
from datetime import datetime
from typing import Any
from procyclingstats import Ranking, Nation, Team, Teams, Rider
import sys


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

        # Add the number of wins for that country for the given year
        country_iso2 = converter.convert(names=nation['nation_name'], to='ISO2')
        country_iso2 = country_iso2 if country_iso2 != 'not found' else nation['nation_name']
        wins_ranking = Ranking(f"nation.php?season={year}&level=1&plevel=smallerorequal&prowin=0&pprowin=largerorequal&filter=Filter&id={country_iso2}&c=me&p=overview&s=nation-wins")
        wins_ranking = wins_ranking.statistics_ranking('rank')

        # Select the first element of the ranking to get the number of wins (just the highest win number)
        if wins_ranking:
            nation['wins'] = wins_ranking[0]['rank']
        else:
            nation['wins'] = 0


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
    except Exception as e:
        print(e)
        sys.exit()

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
    converter = coco.CountryConverter()

    # Build lookup dictionary
    def swap_name(full_name: str) -> str:
        parts = full_name.split()
        for i, part in enumerate(parts):
            if part.isupper():
                # Assume family name starts here
                front_name = " ".join(parts[:i+1])
                family_name = " ".join(parts[i+1:])
                return f"{family_name} {front_name}".upper()
        return ""  # fallback if nothing is all caps

    lookup = {swap_name(r["rider_name"]): r["number_of_wins"] for r in ranking}
    return lookup

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

if __name__ == '__main__':
    pass
