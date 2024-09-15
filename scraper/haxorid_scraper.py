# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from scraper.base_scraper import Scraper


class HaxorIdScraper(Scraper):
    __url = 'https://haxor.id'

    def get_url(self, page):
        if self.attacker:
            attacker = quote_plus(self.attacker)
            attacker = quote_plus(attacker)
            return f'{self.__url}/archive/attacker/{attacker}&page={page}'
        else:
            if self.section == 'archive':
                return f'{self.__url}/{self.section}?page={page}'
            else:
                return f'{self.__url}/archive/{self.section}?page={page}'

    def scrape_links(self, html_content):
        links = []
        soup = BeautifulSoup(html_content, 'html.parser')
        mirror_table = soup.find_all('table', class_='table')
        if not mirror_table and len(mirror_table) < 1:
            raise ValueError
        else:
            try:
                table_body = mirror_table[1].find('tbody')
            except IndexError:
                raise ValueError
            if not table_body:
                raise ValueError
            else:
                table_rows = table_body.find_all('tr')
                if not table_rows:
                    raise ValueError
                else:
                    for row in table_rows:
                        table_data = row.find_all('td')
                        table_data_s = table_data[-3]
                        link = table_data_s.find('a')
                        links.append(link.get('alt'))
        return links
