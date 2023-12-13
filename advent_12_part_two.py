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


def parse_data(data):
    spring_data = []
    for line in data.splitlines():
        springs, numbers = line.split()
        spring_data.append((springs, [int(x) for x in numbers.split(',')]))
    return spring_data


def line_is_viable(line, numbers):
    # Not strict enough, but let's see how it does.
    bad_or_unknown = re.findall('[^.]+', line)
    for bou, length in itertools.zip_longest(bad_or_unknown, numbers):
        if bou is None:
            return False
        if '?' in bou:
            if length is None:
                if '#' not in bou:
                    return True
                return False
            return bou.index('?') <= length
        if len(bou) != length:
            return False
    return True


def test_line_is_viable():
    # Several of these fail, but we only want false positives, not false
    # negatives
    data = [
        ('.###.##.#.', [3, 2, 1], True),
        ('.###.##.#.', [3, 1, 1], False),
        ('.###.##.#.', [3, 2, 1, 1], False),  # this fails; oh well
        ('.#?#.##.#.', [3, 2, 1, 1], False),  # similarly, this fails
        ('.#?#.##.#.', [2, 2, 1], False),  # again, not strict enough
        ('.#?#.##.#.', [4, 2, 1], False),
        ('.###.##?#.', [3, 3, 1], True),
    ]
    for line, nums, expected in data:
        liv = line_is_viable(line, nums)
        testcase = (('True ' if liv == expected else 'False ')
                    + ('positive' if liv else 'negative'))
        print(line, nums, testcase)


def find_parses(line, numbers, debug=False, indent=0):
    if '?' not in line:
        return 1

    parses = 0
    for replacement in ('#', '.'):
        first_unk = line.find('?')
        new_line = line[:first_unk] + replacement + line[first_unk + 1:]
        viable = line_is_viable(new_line, numbers)
        if debug:
            print(' ' * indent, new_line, numbers, viable)
        if viable:
            parses += find_parses(new_line, numbers, debug=debug,
                                  indent=indent + 1)
    return parses


def part_one(data=TEST_CASE, debug=False):
    total_parses = 0
    for pair in parse_data(data):
        parses = find_parses(*pair, debug=debug)
        if debug:
            print('>>>', parses, pair)
        total_parses += parses
    return total_parses


def part_two(data=TEST_CASE, debug=False):
    return 'Nope'


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    test_line_is_viable()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
