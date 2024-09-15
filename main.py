# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import os
import subprocess
import sys
from datetime import datetime

from cli.argument_parser import parse
from scraper.haxorid_scraper import HaxorIdScraper
from scraper.zoneh_scraper import ZoneHScraper
from scraper.zonexsec_scraper import ZoneXsecScraper
from utils.cookie_manager import write_cookies, get_cookie
from utils.log_manager import log_info, log_warn, print_banner, inp, log_error


def is_git_repo(path):
    try:
        subprocess.run(['git', '-C', path, 'status'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def git_pull(path):
    try:
        log_info(f"pulled the latest changes from {path}...")
        subprocess.run(['git', '-C', path, 'pull'], check=True)
        log_info("update successful.")
    except subprocess.CalledProcessError as e:
        log_error(f"failed to attract change: {e}")


def main():
    args = parse()
    time_now = datetime.now()
    time_now = time_now.strftime('%Y_%m_%d_%H_%M_%S')

    section = 'special' if args.special else 'archive' if args.archive else 'onhold' if args.onhold else 'archive' if args.attacker else 'archive'

    print_banner()

    if args.update:
        project_path = os.getcwd()
        if is_git_repo(project_path):
            git_pull(project_path)
        sys.exit()

    log_warn('the program is running. stop the program with just CTRL + C')
    print()

    scraper, output_file = None, ''
    if args.zone_xsec:
        log_info(
            'take a list of links from the site: zone-xsec.com with section page is ' + section)
        output_file = f'zone-xsec_{time_now}.txt'
        scraper = ZoneXsecScraper(
            section=section,
            cache_file='zonexsec_cache.json',
            attacker=args.attacker
        )
    elif args.haxorid:
        log_info(
            'take a list of links from the site: haxor.id with section page is ' + section)
        output_file = f'haxor-id_{time_now}.txt'
        scraper = HaxorIdScraper(
            section=section,
            cache_file='haxor-id_cache.json',
            attacker=args.attacker
        )
    elif args.zone_h:
        log_info(
            'take a list of links from the site: zone-h.org with section page is ' + section)
        if args.zh_zhe and args.zh_phpsessid:
            cookies = {
                'ZHE': args.zh_zhe,
                'PHPSESSID': args.zh_phpsessid
            }
            write_cookies('zone-h.cookie', cookies)
        else:
            if not os.path.isfile('zone-h.cookie'):
                log_warn('cookies not found')
                zhe = inp('please enter ZHE cookie: ')
                phpsessid = inp('please enter PHPSESSID cookie: ')
                cookies = {
                    'ZHE': zhe,
                    'PHPSESSID': phpsessid
                }
                write_cookies('zone-h.cookie', cookies)
            cookies = {
                'ZHE': get_cookie('zone-h.cookie', 'ZHE'),
                'PHPSESSID': get_cookie('zone-h.cookie', 'PHPSESSID')
            }

        log_info(f'cookies: {cookies}')
        output_file = f'zone-h_{time_now}.txt'
        scraper = ZoneHScraper(
            section=section,
            cache_file='zone-h_cache.json',
            attacker=args.attacker,
            cookies=cookies
        )

    if args.attacker:
        log_info(f'retrieve a list of links based on the attacker name: {args.attacker}')

    scraper.output_file = output_file
    min_page, max_page = args.page
    scraper.run(min_page, max_page)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        log_info("CTRL+C detected, program terminated")
