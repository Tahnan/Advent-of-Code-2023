# An unremarkable day 9 (6:37/466th, 10:54/756th); a fairly unremarkable
# problem.  I'm sure there's a faster way to work out polynomial equations,
# but just stepping through things worked just fine.  Debug statements left in
# just to document how lost I got in whether I was adding or subtracting.
from pathlib import Path

import aoc_util

TEST_CASE = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".strip()


def parse_data(data):
    return [[int(x) for x in line.split()] for line in data.splitlines()]


def part_one(data=TEST_CASE, debug=False):
    total = 0
    for line in parse_data(data):
        state = list(line)
        states = []
        # Oh, right... "0" is an error.  That's why I ended up putting in the
        # print(state), and saw an infinite loop of empty states, which led to
        # the "state and" clause, because I didn't realize that my problem was
        # I was supposed to be checking against "{0}".  Fixed that in part 2.
        # Well, that's speed coding for you.
        while state and set(state) != 0:
            if debug:
                print(state)
            states.append(state)
            state = [y - x for x, y in zip(state, state[1:])]
        current = 0
        while states:
            current += states.pop()[-1]
        total += current
    return total


def part_two(data=TEST_CASE, debug=False):
    total = 0
    for line in parse_data(data):
        state = list(line)
        states = []
        while state and set(state) != {0}:
            if debug:
                print(state)
            states.append(state)
            state = [y - x for x, y in zip(state, state[1:])]
        current = 0
        while states:
            if debug:
                print(current, end=' ')
            current = states.pop()[0] - current
        if debug:
            print()
        total += current
    return total


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
