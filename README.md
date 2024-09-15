<h1 align="center">Mizper</h1>
<p align="center">Global Cyber Vandalism Mirror Database Grabber (beta)</p>

## Overview

Mizper is a Python-based project designed to fetch mirror links from websites like:

- https://zone-h.org
- https://zone-xsec.com
- https://haxor.id

Mizper allows users to specify a page or range of pages to scrape, fetches mirror links based on the attacker, and filters the results using cached data to avoid excessive scraping. The project also offers various command line options for flexibility.

### Features

- **Support for multiple sites**: Scrape mirror links from both Zone-H and all.
- **Page range scraping**: Specify `-p/--page` options to scrape a range of pages.
- **Attacker-based scraping**: Use `--attacker` to scrape links based on a specific attacker.
- **Cached results**: Avoid re-scraping previously scraped URLs using a local cache.
- **Command-line interface**: Easy to use with argparse for command-line options.

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package manager)

### Install the required dependencies

```bash
pip install -r requirements.txt
```

**Note**: The scraper requires certain external libraries like `colorama`, `bs4` (BeautifulSoup), and `requests` for scraping and output styling.

## Usage

### Basic Usage

You can run the scraper from the command line with various options.

```bash
python main.py --zone-h --archive --page 1-5
```

This command scrapes pages 1 to 5 from Zone-H.

### Command-line Options

- `-zh/--zone-h`: Scrape the link from https://www.zone-h.org site
- `-zx/--zone-xsec`: Scrape the link from https://www.zone-xsec.com site
- `-hx/--haxorid`: Scrape the link from https://www.haxor.id site
- `-p/--page`: Page number to scraping (if you only want to retrieve 1 page, use `-p/--page 1`, but if there are several pages, use `-p/--page 1-10`)
- `--attacker`: Scrape links based on a specific attacker.
- `-s/--special`: Scrape from the `special` list of mirrors.
- `-a/--archive`: Scrape from the `archive` list of mirrors.
- `-o/--onhold`: Scrape from the `onhold` list of mirrors.

#### Only if scrape links use zone-h

- `--zh-zhe`: set `ZHE` cookie to be able to grab sites in zone-h
- `--zh-phpsessid`: set `PHPSESSID` cookie to be able to grab sites in zone-h

This will produce 1 file called **zone-h.cookie** which contains the ZHE and PHPSESSID cookie formats which will be used for HTTP requests

```text
ZHE=value
PHPSESSID=value
```

You can edit the cookie value directly by editing the contents of the file or by using the options provided

### Example

To scrape Zone-H with section archive pages 1 through 10 and filter results by attacker `anonymous`:

```bash
python main.py --zone-h --archive --page 1-10 --attacker "anonymous"
```

it will automatically generate `output` which will be saved in the output folder and will also be saved in folders based on the part taken/scraped.

### Cache
The mizper utilizes a local cache to store already scraped URLs. This prevents redundant scraping, saving time and resources. Cache management is automatic, and the cache file is updated during each run.

### Error Handling
The mizper includes error handling to ensure smooth execution. Errors such as missing required libraries or network issues are captured and reported to the user.

## Setup and Distribution

You can install the scraper as a command-line tool using setup.py. This will allow you to run it using the `mizper` command directly.

```bash
python setup.py install
```

or

```bash
pip install .
```

## Contributors

Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to submit a pull request or open an issue.