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


class ZoneXsecScraper(Scraper):
    __url = 'https://zone-xsec.com'

    def get_url(self, page):
        if self.attacker:
            attacker = quote_plus(self.attacker)
            return f'{self.__url}/archive/attacker/{attacker}/page={page}'
        else:
            return f'{self.__url}/{self.section}/page={page}'

    def scrape_links(self, html_content):
        links = []
        soup = BeautifulSoup(html_content, 'html.parser')
        mirror_table = soup.find('table', class_='mirror-table')
        if not mirror_table:
            raise ValueError
        else:
            table_body = mirror_table.find('tbody')
            if not table_body:
                raise ValueError
            else:
                table_rows = table_body.find_all('tr')
                if not table_rows:
                    raise ValueError
                else:
                    for row in table_rows:
                        table_data = row.find_all('td')
                        link = table_data[-2]
                        links.append(link.text)
        return links
