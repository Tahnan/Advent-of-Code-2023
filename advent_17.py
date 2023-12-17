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
    final_best = float('inf')
    goal = max(grid)
    # states are (r, c), (dr, dc), <# steps taken in this direction>, <heat>
    states = [((0, 0), (1, 0), 1, 0, ((0, 0),)), ((0, 0), (0, 1), 1, 0, ((0, 0),))]

    steps = 0
    while states:
        # if debug:
        #     print('>>', final_best)
        #     for state in states:
        #         print('    ', state)
        #     steps += 1
        #     if steps > 10:
        #         debug = False
        new_states = []
        for (r, c), (dr, dc), in_this_dir, heat, path in states:
            space = (r + dr, c + dc)
            if space not in grid:
                continue
            heat += grid[space]
            path += ((space, heat),)
            if space == goal:
                final_best = min(final_best, heat)
                if debug:
                    print('>>', final_best)
                    print(path)
                continue
            for drdc, so_far in get_next_states(dr, dc, in_this_dir):
                if best_so_far[(space, drdc, so_far)] <= heat:
                    continue
                best_so_far[(space, drdc, so_far)] = heat
                new_states.append((space, drdc, so_far, heat, path))
        states = new_states
    return final_best


def part_two(data=TEST_CASE, debug=False):
    pass


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
