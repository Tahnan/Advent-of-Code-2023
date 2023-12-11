# Day 11: 18:13 (1741), 20:29 (999)
# Why so long?  Because when I copied the test case, I accidentally lost the
# trailing period, and Grid.get_row() therefore thought there was one less
# column than there actually was and reported row 7, which has a galaxy in the
# last column, as blank.  So I sat there trying to find the bug in code that
# was functioning perfectly fine.
#
# Let this be a lesson, kids: never write tests for your code.
import itertools
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".strip()


def expanded_manhattan(c1, c2, empty_rows, empty_cols, expansion=2):
    # Manhattan distance, with empty rows and empty columns expanded by a given
    # factor
    xs, ys = zip(c1, c2)
    min_x, max_x = sorted(xs)
    min_y, max_y = sorted(ys)
    e_rows = len({r for r in empty_rows if min_x < r < max_x})
    e_cols = len({c for c in empty_cols if min_y < c < max_y})
    return ((max_x - min_x) + (max_y - min_y)
            + e_rows * (expansion - 1)
            + e_cols * (expansion - 1))


def parse_data(data):
    space = Grid.from_text(data)
    empty_rows = set()
    empty_columns = set()
    for row in range(space.rows):
        if set(space.get_row(row)) == {'.'}:
            empty_rows.add(row)
    for col in range(space.columns):
        if set(space.get_column(col)) == {'.'}:
            empty_columns.add(col)
    return space, empty_rows, empty_columns


def part_one(data=TEST_CASE, debug=False, expansion=2):
    space, empty_rows, empty_cols = parse_data(data)
    galaxies = {coord for coord, content in space.items() if content == '#'}
    distance = 0
    for pair in itertools.combinations(galaxies, 2):
        this_dist = expanded_manhattan(*pair, empty_rows, empty_cols,
                                       expansion=expansion)
        distance += this_dist
    return distance


def part_two(data=TEST_CASE, debug=False):
    return part_one(data=data, debug=debug, expansion=1000000)


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
