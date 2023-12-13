# Day 13: 18:22 (889), 22:57 (536)
#
# One of those days where I was fine until the last line, when I returned the
# wrong number, and then lost time debugging the code leading up to it.
#
# The Grid class helped immensely here.  I hated the copy-paste from part one
# to part two, but it was way faster than trying to factor things out.  (For
# that matter, the copy-paste from "row" to "col" wasn't great, but when you're
# calling a slightly different function on the class and adding the result to
# a different constant, it's just a little harder to do some sort of "for
# row_or_col in (row, col):" that captures both.

from grid_util import Grid
from pathlib import Path

import aoc_util

TEST_CASE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    return [Grid.from_text(pattern) for pattern in data.split('\n\n')]


def part_one(data=TEST_CASE, debug=False):
    horiz = 0
    vert = 0
    for grid in parse_data(data):
        for col_num in range(grid.columns):
            check = 0
            while 0 <= col_num - (check + 1) < col_num + check < grid.columns:
                left = grid.get_column(col_num - (check + 1))
                right = grid.get_column(col_num + check)
                if left != right:
                    break
                check += 1
            else:
                if debug:
                    print('C:', col_num)
                vert += col_num
        for row_num in range(grid.rows):
            check = 0
            while 0 <= row_num - (check + 1) < row_num + check < grid.rows:
                top = grid.get_row(row_num - (check + 1))
                bottom = grid.get_row(row_num + check)
                if top != bottom:
                    break
                check += 1
            else:
                if debug:
                    print('R:', row_num)
                horiz += row_num
    return 100 * horiz + vert


def part_two(data=TEST_CASE, debug=False):
    horiz = 0
    vert = 0
    for grid in parse_data(data):
        for col_num in range(grid.columns):
            check = 0
            smudges = 0
            while 0 <= col_num - (check + 1) < col_num + check < grid.columns:
                left = grid.get_column(col_num - (check + 1))
                right = grid.get_column(col_num + check)
                diffs = sum(x != y for x, y in zip(left, right))
                if diffs > 1:
                    break
                smudges += diffs
                check += 1
            else:
                if smudges == 1:
                    vert += col_num
        for row_num in range(grid.rows):
            check = 0
            smudges = 0
            while 0 <= row_num - (check + 1) < row_num + check < grid.rows:
                top = grid.get_row(row_num - (check + 1))
                bottom = grid.get_row(row_num + check)
                diffs = sum(x != y for x, y in zip(top, bottom))
                if diffs > 1:
                    break
                smudges += diffs
                check += 1
            else:
                if smudges == 1:
                    horiz += row_num
    return 100 * horiz + vert


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
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
