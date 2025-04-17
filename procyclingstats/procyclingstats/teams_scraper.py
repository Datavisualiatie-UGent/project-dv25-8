from typing import List
from .scraper import Scraper

class Teams(Scraper):
    def __init__(self):
        super().__init__('teams.php?year=2025&filter=Filter&s=worldtour', update_html=False);

    def teams(self, year: int) -> List[str]:
        self.year = year

        self._url = self._make_url_absolute(f'teams.php?year={year}&filter=Filter&s=worldtour')
        self.update_html()

        teams = []
        html_ul = self.html.css_first('span.table-cont > ul')
        for li in html_ul.css('li'):
            teams.append(li.css_first('div > a').attributes.get('href'))
        return teams
