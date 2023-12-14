from enum import Enum
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip()


def tilt_grid(grid, direction, debug=False):
    grid = Grid(grid)
    dr, dc = direction
    if dc == 0:
        rownums = range(grid.rows)
        if dr == 1:
            rownums = reversed(rownums)
        for r in rownums:
            for c in range(grid.columns):
                contents = grid[(r, c)]
                if contents != 'O':
                    continue
                if debug:
                    print(f'From {(r, c)} to ', end='')
                grid[(r, c)] = '.'
                new_r = r
                while (0 <= new_r < grid.rows and
                       grid.get((new_r + dr, c)) == '.'):
                    new_r += dr
                grid[(new_r, c)] = 'O'
                if debug:
                    print((new_r, c))
    else:
        colnums = range(grid.columns)
        if dc == 1:
            colnums = reversed(colnums)
        for c in colnums:
            for r in range(grid.rows):
                contents = grid[(r, c)]
                if contents != 'O':
                    continue
                grid[(r, c)] = '.'
                new_c = c
                while (0 <= new_c < grid.columns and
                       grid.get((r, new_c + dc)) == '.'):
                    new_c += dc
                grid[(r, new_c)] = 'O'
    return grid


def parse_data(data):
    return Grid.from_text(data)


def measure_weight_on_north(grid):
    weight = 0
    for (row, col), contents in grid.items():
        if contents == 'O':
            weight += grid.rows - row
    return weight


def part_one(data=TEST_CASE, debug=False):
    grid = tilt_grid(parse_data(data), (-1, 0), debug=debug)
    if debug:
        print(grid.to_text())
    return measure_weight_on_north(grid)


def get_rock_positions(grid):
    return tuple(sorted(coord for coord, contents in grid.items()
                        if contents == 'O'))


def part_two(data=TEST_CASE, debug=False):
    cycles = 1000000000
    grid = parse_data(data)
    seen_positions = {get_rock_positions(grid): -1}
    for cycle_num in range(1, cycles):
        # We're not really going through all of these
        for d in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            grid = tilt_grid(grid, d)
        if debug:
            print('Cycle', cycle_num)
            print(grid.to_text())
            print('---')
        positions = get_rock_positions(grid)
        if positions in seen_positions:
            cycle_start = seen_positions[positions]
            cycle_length = cycle_num - cycle_start
            final_point = (cycle_start + ((cycles - cycle_start) % cycle_length))
            final_positions, = [pos for pos, num in seen_positions.items()
                                if num == final_point]
            weight = 0
            for row, _ in final_positions:
                weight += grid.rows - row
            return weight
        seen_positions[positions] = cycle_num


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
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
