# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import os


def read_cookies(file_path):
    cookies = {}
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '=' in line:
                    name, value = line.split('=', 1)
                    cookies[name] = value
    return cookies


def write_cookies(file_path, cookies):
    with open(file_path, 'w', encoding='utf-8') as file:
        for name, value in cookies.items():
            file.write(f"{name}={value}\n")


def get_cookie(file, name):
    cookies = read_cookies(file)
    return cookies.get(name)