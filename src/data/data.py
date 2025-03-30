import country_converter as coco
import diskcache
from typing import Any
from procyclingstats import Ranking

cache = diskcache.Cache(".cache")

@cache.memoize()
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

@cache.memoize()
def get_riders(year: int, nation_name: str) -> list[dict[str, Any]]:
    # Convert the country name to iso2 to use in the filter
    converter = coco.CountryConverter()
    country_iso2 = converter.convert(names=nation_name, to='ISO2')
    country_iso2 = country_iso2 if country_iso2 != 'not found' else nation_name

    # Get the riders
    riders = Ranking(f"nation.php?season={year}&level=wt&filter=Filter&id={country_iso2}&c=me&p=overview&s=contract-riders")
    riders = riders.individual_ranking('rider_name', 'team_name')

    return riders

@cache.memoize()
def get_average_age(year: int) -> list[dict[str, Any]]:
    ranking = Ranking(f"statistics.php?year={year}&level=1&sekse=1&filter=Filter&p=teams&s=average-age")
    ranking = ranking.statistics_ranking('rank', 'team_name', 'average_age')
    return ranking

@cache.memoize()
def get_youngest_age(year: int) -> list[dict[str, Any]]:
    ranking = Ranking(f"statistics.php?year={year}&sekse=1&level=1&filter=Filter&p=riders&s=youngest-riders")
    ranking = ranking.statistics_ranking('rank', 'rank', 'rider_name', 'min_age')
    return ranking
