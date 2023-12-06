# Day 6: 5:10 (546th); 8:19 (671st)
# The calculation in part two is really the smarter way to do part one and I
# should have done it that way in the first place.
from pathlib import Path

import aoc_util

TEST_CASE = """
Time:      7  15   30
Distance:  9  40  200
""".strip()


def parse_data(data):
    racetime, distance = data.splitlines()
    racetime = [int(x) for x in racetime.split()[1:]]
    distance = [int(x) for x in distance.split()[1:]]
    return list(zip(racetime, distance))


def part_one(data=TEST_CASE, debug=False):
    ways_to_win = 1
    for racetime, distance in parse_data(data):
        ways_to_win_this_race = 0
        for hold in range(racetime):
            if hold * (racetime - hold) > distance:
                ways_to_win_this_race += 1
        ways_to_win *= ways_to_win_this_race
    return ways_to_win


def part_two(data=TEST_CASE, debug=False):
    racetime, distance = data.splitlines()
    racetime = int(''.join(racetime.split()[1:]))
    distance = int(''.join(distance.split()[1:]))
    for min_hold in range(racetime):
        if min_hold * (racetime - min_hold) > distance:
            break
    for max_hold in range(racetime, 0, -1):
        if max_hold * (racetime - max_hold) > distance:
            break
    return max_hold - min_hold + 1


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
