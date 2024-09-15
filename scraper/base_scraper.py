# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import os
import random
import requests

from utils.cache_manager import CacheManager

from utils.log_manager import log_info, log_sucs, log_error, truncate_text


class Scraper:
    """ Base class for scraping """

    def __init__(self, section, cache_file, attacker=None, cookies=None):
        self.section = section
        self.attacker = attacker
        self.cookies = cookies
        self.cache_manager = CacheManager(cache_file)
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 "
            "Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 "
            "Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/14.0"
            "Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 "
            "Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.36"
        ]
        self.output_links = []
        self.output_file = None

    def get_url(self, page):
        """ Generate the URL for the scraper """
        raise NotImplementedError('Subclasses must implement the get_url method.')

    def request(self, url):
        headers = {'User-Agent': random.choice(self.user_agent)}
        if self.cookies:
            session = requests.Session()
            session.cookies.update(self.cookies)
            resp = session.get(url=url, headers=headers, cookies=self.cookies)
        else:
            resp = requests.get(url=url, headers=headers)
        resp.raise_for_status()
        return resp

    def fetch_page(self, page):
        """ Fetch the HTML content of the page """
        url = self.get_url(page)
        try:
            response = self.request(url)
            log_sucs(truncate_text(f'successfully fetched page {page} from {url}'))
            return response.text
        except requests.RequestException as error:
            log_error(f'error fetching page {page}: {error}')
            return None

    def scrape_links(self, html_content):
        """ Extract links from HTML content """
        raise NotImplementedError('Subclasses must implement the get_url method.')

    def process_pages(self, start_page, end_page):
        """ Process a range of pages """
        index = None
        try:
            log_info('please wait, this may take a while depending on the speed of your internet connection')
            for page in range(start_page, end_page + 1):
                index = page
                html_content = self.fetch_page(page)
                if html_content:
                    links = self.scrape_links(html_content=html_content)
                    for link in links:
                        link_str = str(link)
                        link_str = self.__get_domain(link_str)
                        if not self.cache_manager.is_link_cached(link=link_str):
                            self.cache_manager.add_link_to_cache(link=link_str)
                            self.output_links.append(link_str)
                del html_content
        except ValueError:
            log_error(f'link not found on page {index}, this may not be until it has {index} pages')
            return None
        except PermissionError as error:
            log_error(error)
            return None

    def save_output(self, file_path):
        """ Save the scraped links to a text file """
        if not os.path.exists('output'):
            os.makedirs('output')
        if not os.path.exists(f'output/{self.section}'):
            os.makedirs(f'output/{self.section}')

        filename = f'output/{self.section}/{file_path}'
        with open(filename, 'w') as file:
            for link in self.output_links:
                file.write(f"{link}\n")
        log_sucs(f'result saved to: {filename}')

    @staticmethod
    def __get_domain(url):
        path_start = url.find('/')
        if path_start == -1:
            domain = url
        else:
            domain = url[:path_start]

        port_start = url.find(':')
        if port_start != -1:
            domain = domain[:port_start]

        return domain

    def run(self, start_page, end_page):
        """ Run the scraper for the specified page range """
        log_info(f'starting scraping from page {start_page} to page {end_page}')
        self.process_pages(start_page, end_page)
        if len(self.output_links) > 0:
            log_info(f'scraping completed. total links found: {len(self.output_links)}')
            if self.output_file:
                self.save_output(self.output_file)
        else:
            log_error(f'scraping failed. no links found')
