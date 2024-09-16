# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import re
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

from scraper.base_scraper import Scraper


class ZoneHScraper(Scraper):
    __url = 'https://www.zone-h.org'

    def get_url(self, page):
        if self.attacker:
            attacker = quote_plus(self.attacker)
            return f'{self.__url}/archive/notifier={attacker}/page={page}'
        else:
            section = self.section
            if section == 'archive':
                return f'{self.__url}/archive/page={page}'
            elif section == 'special':
                return f'{self.__url}/archive/special=1/page={page}'
            elif section == 'onhold':
                return f'{self.__url}/archive/published=0/page={page}'
            else:
                return f'{self.__url}/archive/page={page}'

    def scrape_links(self, html_content):
        links = []
        soup = BeautifulSoup(html_content, 'html.parser')
        captcha = soup.get_text(separator=' ', strip=True)
        if 'If you often get this captcha when gathering data' in captcha:
            captcha = True
        else:
            captcha = False
        if captcha is False:
            mirror_table = soup.find('table', {'id': 'ldeface'})
            if not mirror_table:
                raise ValueError
            else:
                table_rows = mirror_table.find_all('tr')
                if not table_rows:
                    raise ValueError
                else:
                    if len(table_rows) >= 8:
                        for row in table_rows:
                            table_data = row.find_all('td')
                            for tbl in table_data:
                                data = re.findall('<td>(.*)\n							</td>', str(tbl))
                                for dt in data:
                                    links.append(dt)
        else:
            raise PermissionError('captcha detected, please visit the site https://zone-h.org then complete the captcha and retrieve the ZHE and PHPSESSID cookies then reset the cookies with the --zh-zhe and --zh-phpsessid options')
        return links
