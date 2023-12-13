import itertools
import re
from pathlib import Path

import aoc_util

TEST_CASE = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".strip()

BAD_SPRINGS = re.compile('#+')


def parse_data(data):
    spring_data = []
    for line in data.splitlines():
        springs, numbers = line.split()
        spring_data.append((springs, [int(x) for x in numbers.split(',')]))
    return spring_data


def interpolate(line, faulty_positions):
    faulty_num = 0
    reline = ''
    for spring in line:
        if spring == '?':
            reline += '#' if faulty_num in faulty_positions else '.'
            faulty_num += 1
        else:
            reline += spring
    return reline


def find_parses(line, numbers):
    parses = 0

    # oh god this is so brute force
    perm_seen = set()
    known_faulty = line.count('#')
    unknowns = line.count('?')
    unknown_faulty = sum(numbers) - known_faulty

    unknowns_order = list(range(unknowns))
    for faulty in itertools.combinations(unknowns_order, unknown_faulty):
        real_line = interpolate(line, faulty)
        bad_springs = [len(x) for x in BAD_SPRINGS.findall(real_line)]
        if bad_springs == numbers:
            parses += 1
    return parses


def part_one(data=TEST_CASE, debug=False):
    total_parses = 0
    for pair in parse_data(data):
        total_parses += find_parses(*pair)
    return total_parses


def part_two(data=TEST_CASE, debug=False):
    # Nope.  This is O(heat death of the universe).  Trying again, new file.
    total_parses = 0
    for springs, numbers in parse_data(data):
        springs = '?'.join([springs] * 5)
        numbers = numbers * 5
        total_parses += find_parses(springs, numbers)
    return total_parses


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
