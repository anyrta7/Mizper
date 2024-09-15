# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.

import json
import os.path


class CacheManager:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """ Load cache from JSON file """
        if not os.path.exists(self.cache_file):
            # Return empty set if cache file does not exists
            return set()
        try:
            with open(self.cache_file, 'r') as file:
                data = file.read()
                if data:
                    return set(json.loads(data))
                else:
                    return set()
        except json.JSONDecodeError as error:
            print(f'Error loading cache file: {error}')
            # Return empty set on error
            return set()

    def save_cache(self):
        """ Save cache to a JSON file """
        if not os.path.exists('.cache'):
            os.makedirs('.cache')

        with open(os.path.join('.cache', self.cache_file), 'w') as file:
            json.dump(list(self.cache), file)

    def is_link_cached(self, link):
        """ Check if a link is in the cache """
        return link in self.cache

    def add_link_to_cache(self, link):
        """ Add a link to the cache """
        if link not in self.cache:
            self.cache.add(link)
            self.save_cache()