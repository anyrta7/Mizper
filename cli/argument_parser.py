# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import re
from argparse import ArgumentParser, SUPPRESS
from argparse import RawTextHelpFormatter


def parse_limit(input_str):
    if '-' in input_str:
        try:
            min_value, max_value = input_str.split('-')
            min_value = int(min_value)
            max_value = int(max_value)
        except ValueError:
            raise ValueError("invalid input'.")
    else:
        min_value = max_value = int(input_str)

    return min_value, max_value


def get_version_from_setup():
    try:
        with open("setup.py", "r") as f:
            setup_content = f.read()
            version_match = re.search(r"version=['\"]([^'\"]+)['\"]", setup_content)
            if version_match:
                return version_match.group(1)
            else:
                return "version not found on setup.py"
    except FileNotFoundError:
        return "setup.py not found"


def parse():
    parser = ArgumentParser(
        prog='mizper',
        usage='%(prog)s -h/--help',
        description="(Mirror Scraper) Global Cyber Vandalism Mirror Database Grabber\n"
                    "This tool is used to retrieve a list of links to sites that have been hacked and has been "
                    "included in a global vandalism site mirror database.\n"
                    "@Anyrta7 - @SandsX",
        epilog='example usage:\n'
               'mizper --zone-xsec --archive --page 1-9\n'
               'mizper --haxorid --atacker "anonymous" --special --page 5-10\n\n'
               'for zone-h, cookies are required, so if cookies have not been set in config.yaml then enter the '
               'following parameter options\n'
               'mizper --zone-h --archive --page 5 --zh-zhe COOKIE --zh-phpsessid COOKIE',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s version {get_version_from_setup()}')
    parser.add_argument('-u', '--update', action='store_true', help='update from github project')
    site = parser.add_argument_group('sites',
                                     'Global Cyber Vandalism Mirror Database site from which a list of links will be '
                                     'taken')
    site.add_argument('-zh', '--zone-h', action='store_true', help=f'scrape the link from https://www.zone-h.org site')
    site.add_argument('-hx', '--haxorid', action='store_true',
                      help=f'scrape the link from https://haxor.id site')
    site.add_argument('-zx', '--zone-xsec', action='store_true',
                      help=f'scrape the link from https://zone-xsec.com site')

    section = parser.add_argument_group('section',
                                        'section page that will be searched and retrieved the list of URL links')
    section.add_argument('-s', '--special', action='store_true', help='get the link from special page section')
    section.add_argument('-a', '--archive', action='store_true', help='get the link from archive page section')
    section.add_argument('-o', '--onhold', action='store_true', help='get the link from onhold page section')

    parser.add_argument('-p', '--page', type=parse_limit, default='1', help='page number to scraping (default: %('
                                                                            'default)s)')
    parser.add_argument('--attacker', type=str, help='get the link based on specific attacker name')

    parser.add_argument('--zh-zhe', help=SUPPRESS)
    parser.add_argument('--zh-phpsessid', help=SUPPRESS)

    args = parser.parse_args()

    selected_site = [option for option in [args.zone_xsec, args.zone_h, args.haxorid] if option]
    if len(selected_site) != 1:
        parser.error('only one option is allowed between -zh/--zone-h, -hx/--haxorid, dan -zx/--zone-xsec.')

    if args.attacker:
        if args.onhold or args.special:
            parser.error('if the --attacker option is entered then you cannot use the -o/--onhold and -s/--special '
                         'options, only the -a/--archive option can be used')
    else:
        selected_section = [option for option in [args.archive, args.onhold, args.special] if option]
        if len(selected_section) != 1:
            parser.error('only one option is allowed between -a/--archive, -s/--special, dan -o/--onhold.')

    return args
