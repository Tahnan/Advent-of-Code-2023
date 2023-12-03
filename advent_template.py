from pathlib import Path

import aoc_util

TEST_CASE = """
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    pass


def part_one(data=TEST_CASE, debug=False):
    pass


def part_two(data=TEST_CASE, debug=False):
    pass


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    print(time.ctime(), part_one())
    print(time.ctime(), part_one(data=DATA))
    print(time.ctime(), part_two())
    print(time.ctime(), part_two(data=DATA))
