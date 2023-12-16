# Day 16: 24:02 (1038), 32:37 (1139)
# On my first run of the code, I got the right answer for the test case for
# part one, and for the actual data, I got "9".  Which seemed *awfully* low.
# (It was.)  Turns out that starting at (0, 0) was great *as long as (0, 0) was
# an empty space*, which in my input, it was not.
#
# Of course, I also lost some time wrangling backslashes.  Come on, man.

from pathlib import Path

import aoc_util
from grid_util import Grid

# It won't matter in the data read from file, but the backslash problems in the
# tast case are driving me *nuts*.
SLASH = '╱'  # U+2571 Box Drawings Light Diagonal Upper Right To Lower Left
BACKSLASH = '╲'  # U+2572 as above

TEST_CASE = """
.|...╲....
|.-.╲.....
.....|-...
........|.
..........
.........╲
..../.╲╲..
.-.-/..|..
.|....-|.╲
..//.|....
""".strip()


MIRRORS = {
    SLASH: {(-1, 0): (0, 1),
            (0, 1): (-1, 0),
            (1, 0): (0, -1),
            (0, -1): (1, 0)},
    BACKSLASH: {(-1, 0): (0, -1),
                (0, -1): (-1, 0),
                (1, 0): (0, 1),
                (0, 1): (1, 0)}
}


def parse_data(data):
    return Grid.from_text(
        data.replace('/', SLASH).replace('\\', BACKSLASH)
    )


def energize_grid(layout, current_states, debug=False):
    energized = set()
    # states are (coord, drdc)
    seen_states = set(current_states)
    while True:
        new_states = []
        for (r, c), (dr, dc) in current_states:
            new_coord = (r + dr, c + dc)
            if new_coord not in layout:
                continue
            contents = layout[new_coord]
            if contents == '|' and dr == 0:
                newest_states = [
                    (new_coord, (1, 0)),
                    (new_coord, (-1, 0))
                ]
            elif contents == '-' and dc == 0:
                newest_states = [
                    (new_coord, (0, -1)),
                    (new_coord, (0, 1))
                ]
            elif contents in MIRRORS:
                newest_states = [(new_coord, MIRRORS[contents][(dr, dc)])]
            else:
                newest_states = [(new_coord, (dr, dc))]
            new_states.extend([state for state in newest_states
                               if state not in seen_states])
            seen_states.update(newest_states)
            energized.add(new_coord)
        if not new_states:
            return len(energized)
        if debug:
            print(len(energized), new_states)
        current_states = new_states


def part_one(data=TEST_CASE, debug=False):
    layout = parse_data(data)
    current_states = [((0, -1), (0, 1))]
    # OK, yes, this entire function got factored out during part two
    return energize_grid(layout, current_states, debug=debug)


def part_two(data=TEST_CASE, debug=False):
    layout = parse_data(data)
    max_energy = 0
    for r in range(layout.rows):
        for c in (-1, layout.columns):
            start = [((r, c), (0, 1 if c == -1 else -1))]
            if debug:
                print(start)
            energy = energize_grid(layout, start, debug=debug)
            max_energy = max(max_energy, energy)
    for c in range(layout.columns):
        for r in (-1, layout.rows):
            start = [((r, c), (1 if r == -1 else -1, 0))]
            if debug:
                print(start)
            energy = energize_grid(layout, start, debug=debug)
            max_energy = max(max_energy, energy)
    return max_energy


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    for fn, kwargs in (
        (part_one, {}),
        (part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
