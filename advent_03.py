# Notes:
# * Man, I just floundered my way through this one.  It didn't help that I
#   misread the task by missing that diagonals counted (which honestly made
#   things easier).  I'm accustomed to working with grids, but not to working
#   with single entities that span more than one cell of a grid.
# * After all that, it still feels like a total mess.

from pathlib import Path
import re

import aoc_util

TEST_CASE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()


def _is_symbol(char):
    # This got pulled out as a helper before _has_symbol_neighbor got (a)
    # factored out and (b) rewritten to be a single nested for-loop instead of
    # a more complicated thing.  It could be inlined, but it's a sensible
    # function, so let's leave it here for historical purposes.
    return char != '.' and not char.isdigit()


def _has_symbol_neighbor(rownum, colspan, data):
    rowlen = len(data[0])
    start, end = colspan
    # "d" as in "delta".  There's a dance to ensure that we're not using -1
    # (which would get the far end of the row/col) or too large a number (which
    # would get an IndexError).
    for drow in (-1, 0, 1):
        for col in range(max(start - 1, 0), min(end + 1, rowlen)):
            row = rownum + drow
            if not 0 <= row < rowlen:
                continue
            if _is_symbol(data[row][col]):
                return True
    return False


def part_one(data=TEST_CASE, debug=False):
    total = 0
    data = data.splitlines()
    for rownum, line in enumerate(data):
        for digits in re.finditer(r'\d+', line):
            number = int(digits.group())
            if _has_symbol_neighbor(rownum, digits.span(), data):
                total += number
    return total


def part_two(data=TEST_CASE, debug=False):
    total = 0
    data = data.splitlines()

    # Pairs, not a dict, in case a number appears more than once
    numbers = [
        (int(digits.group()), {(rownum, c) for c in range(*digits.span())})
        for rownum, line in enumerate(data)
        for digits in re.finditer(r'\d+', line)
    ]

    for rownum, line in enumerate(data):
        for colnum, char in enumerate(line):
            if char == '*':
                # We don't need the same caution necessary in
                # _has_symbol_neighbor, because coordinates outside the grid
                # will simply fail to ever appear in the numbers' coords
                gearbox = {
                    (rownum + drow, colnum + dcol)
                    for drow in (-1, 0, 1)
                    for dcol in (-1, 0, 1)
                }
                adjacent = [
                    number for number, location in numbers
                    if location & gearbox
                ]
                if len(adjacent) == 2:
                    total += adjacent[0] * adjacent[1]
    return total


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
