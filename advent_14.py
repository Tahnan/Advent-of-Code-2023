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


def parse_data(data):
    return Grid.from_text(data)


def tilt_grid(grid, direction, debug=False):
    # I hope this is self-evident, because I'm not sure I have the energy to
    # walk through it in a comment.
    grid = Grid(grid)
    dr, dc = direction

    # Have *got* to find a way to do the "row or column, whichever" thing
    if dc == 0:
        rownums = range(grid.rows)
        if dr == 1:
            rownums = reversed(rownums)
        for r in rownums:
            for c in range(grid.columns):
                contents = grid[(r, c)]
                if contents != 'O':
                    continue
                grid[(r, c)] = '.'
                new_r = r
                while (0 <= new_r < grid.rows and
                       grid.get((new_r + dr, c)) == '.'):
                    new_r += dr
                grid[(new_r, c)] = 'O'
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


def get_rock_positions(grid):
    return tuple(sorted(coord for coord, contents in grid.items()
                        if contents == 'O'))


def measure_weight_on_north(rock_positions, grid_height):
    weight = 0
    for row, _ in rock_positions:
        weight += grid_height - row
    return weight


def part_one(data=TEST_CASE, debug=False):
    grid = tilt_grid(parse_data(data), (-1, 0))
    if debug:
        print(grid.to_text())
    return measure_weight_on_north(get_rock_positions(grid), grid.rows)


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)
    cycles = 1000000000
    cycle_num = 0
    seen_positions = {get_rock_positions(grid): cycle_num}
    while True:
        # There are a finite number of possible positions.  Even more to the
        # point, there's a smaller number of finite positions where everything
        # is as far north as it can go.  That number has *got* to be smaller
        # than "one billion", so find the point where we're in a position we've
        # seen before, and do the modular arithmetic.
        cycle_num += 1
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
            return measure_weight_on_north(final_positions, grid.rows)
        seen_positions[positions] = cycle_num


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
