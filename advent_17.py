# Day 17.  17:16:14 (13521), 17:25:37 (12374).  So yeah.
#
# Spent a lot of time trying to decide which was worse, the fact that I got the
# wrong answer on the test data or the fact that I got no answer on the full
# data.  Probably the latter.  Set it aside (obviously), came back with a much
# better plan for going through the paths.
#
# Hey, I wonder if this would help with last year's elephants.

from collections import defaultdict
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".strip()


ANOTHER_TEST = """111111111111
999999999991
999999999991
999999999991
999999999991
""".strip()


def parse_data(data):
    grid = Grid.from_text(data)
    return Grid({x: int(y) for x, y in grid.items()})


def get_next_states(dr, dc, in_this_dir):
    new_states = [((dc, -dr), 1), ((-dc, dr), 1)]
    if in_this_dir < 3:
        new_states.append(((dr, dc), in_this_dir + 1))
    return new_states


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)

    best_so_far = defaultdict(lambda: float('inf'))
    goal = max(grid)
    # states are (r, c), (dr, dc), <# steps taken in this direction>, <path>
    states = [((0, 0), (1, 0), 1, ((0, 0),)), ((0, 0), (0, 1), 1, ((0, 0),))]
    heat_map = defaultdict(list)
    heat_map[0] = states

    current_heat = 0
    while True:
        while current_heat not in heat_map:
            current_heat += 1
        states = heat_map.pop(current_heat)
        for (r, c), (dr, dc), in_this_dir, path in states:
            space = (r + dr, c + dc)
            if space not in grid:
                continue
            new_heat = current_heat + grid[space]
            path += ((space, new_heat),)
            if space == goal:
                if debug:
                    print(path)
                return new_heat
            for drdc, so_far in get_next_states(dr, dc, in_this_dir):
                if best_so_far[(space, drdc, so_far)] <= new_heat:
                    continue
                best_so_far[(space, drdc, so_far)] = new_heat
                heat_map[new_heat].append((space, drdc, so_far, path))


def get_next_ultra_states(dr, dc, in_this_dir):
    new_states = []
    if in_this_dir >= 4:
        new_states = [((dc, -dr), 1), ((-dc, dr), 1)]
    if in_this_dir < 10:
        new_states.append(((dr, dc), in_this_dir + 1))
    return new_states


def part_two(data=TEST_CASE, debug=False):
    grid = parse_data(data)

    best_so_far = defaultdict(lambda: float('inf'))
    goal = max(grid)
    # states are (r, c), (dr, dc), <# steps taken in this direction>, <path>
    states = [((0, 0), (1, 0), 1, ((0, 0),)), ((0, 0), (0, 1), 1, ((0, 0),))]
    heat_map = defaultdict(list)
    heat_map[0] = states

    current_heat = 0
    while True:
        while current_heat not in heat_map:
            current_heat += 1
        states = heat_map.pop(current_heat)
        for (r, c), (dr, dc), in_this_dir, path in states:
            space = (r + dr, c + dc)
            if space not in grid:
                continue
            new_heat = current_heat + grid[space]
            path += ((space, new_heat),)
            if space == goal:
                if in_this_dir >= 4:
                    if debug:
                        print(path)
                    return new_heat
            for drdc, so_far in get_next_ultra_states(dr, dc, in_this_dir):
                if best_so_far[(space, drdc, so_far)] <= new_heat:
                    continue
                best_so_far[(space, drdc, so_far)] = new_heat
                heat_map[new_heat].append((space, drdc, so_far, path))
        if debug:
            print('Current heat:', current_heat)
            for heat, states in sorted(heat_map.items()):
                print(' ', heat, len(states))


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
        (part_two, {'data': ANOTHER_TEST}),
        (part_two, {}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
