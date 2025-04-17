from .scraper import Scraper

class Nation(Scraper):
    def __init__(self, year: int, nation_url: str):
        super().__init__('???', update_html=False)
        self.year = year
        self.nation_url = nation_url

    def name(self):
        return self.nation_url.split('/')[1]

    def teams(self):
        self._url = self._make_url_absolute(f'nation.php?season={self.year}&filter=Filter&id={self.name()}&c=me&p=overview&s=teams')
        self.update_html()

        teams = []
        html_table = self.html.css_first('span.table-cont > table')
        for html_tr in html_table.css_first('tbody').css('tr'):
            if html_tr.css('td')[2].text() != 'WT':
                continue
            teams.append(html_tr.css('td')[1].css_first('a').attributes.get('href'))
        return teams

    def riders(self):
        self._url = self._make_url_absolute(f'nation.php?season={self.year}&level=wt&filter=Filter&id={self.name()}&c=me&p=overview&s=contract-riders')
        self.update_html()

        riders = []
        html_table = self.html.css_first('span.table-cont > table')
        for html_tr in html_table.css_first('tbody').css('tr'):
            riders.append(html_tr.css('td')[1].css_first('a').attributes.get('href'))
        return riders

    def wins(self):
        self._url = self._make_url_absolute(f'nation.php?season={self.year}&level=1&plevel=smallerorequal&prowin=0&pprowin=largerorequal&filter=Filter&id={self.name()}&c=me&p=overview&s=nation-wins')
        self.update_html()

        try:
            text = self.html.css_first('table > tbody > tr > td').text()
            if text.isdigit():
                return int(text)
        except:
            return 0
        return 0

    def pcs_points(self):
        self._url = self._make_url_absolute(f'nation.php?date={self.year}-12-31&filter=Filter&id={self.name()}&c=me&p=overview&s=pcs-ranking')
        self.update_html()

        try:
            text = self.html.css_first('tbody > tr.sum').css('td')[4].text()
            if text.isdigit():
                return int(text)
        except:
            return 0
        return 0
