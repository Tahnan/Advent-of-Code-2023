import requests
from pathlib import Path

with (Path(__file__).parent / 'aoc_cookie.txt').open() as f:
    COOKIE = f.read()

SESSION = requests.Session()
SESSION.headers.update(
    {'Accept-Encoding': 'gzip, deflate, br',
     'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                'image/avif,image/webp,*/*;q=0.8'),
     'Cookie': COOKIE}
)


def _input_file(day):
    return Path(__file__).parent / f'input_{str(day).zfill(2)}.txt'


def _fetch_input(day):
    print('Fetching input')
    response = SESSION.get(
        f'https://adventofcode.com/2023/day/{int(day)}/input'
    )
    response.raise_for_status()
    return response.text


def get_input_file(day):
    # If (and only if) the file doesn't already exist, download it[len
    input_file = _input_file(day)
    if not input_file.exists():
        with _input_file(day).open('w') as f:
            f.write(_fetch_input(day))
    return input_file
