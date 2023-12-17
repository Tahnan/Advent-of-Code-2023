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


def get_turns(dr, dc):
    return [(dc, -dr), (-dc, dr)]


def part_one(data=TEST_CASE, debug=False):
    grid = parse_data(data)

    best_so_far = defaultdict(lambda: float('inf'))
    final_best = float('inf')
    goal = max(grid)
    # states are (r, c), (dr, dc), <# steps taken in this direction>, <heat>
    states = [((0, 0), (1, 0), 0, 0), ((0, 0), (0, 1), 0, 0)]

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
        for (r, c), (dr, dc), in_this_dir, heat_so_far in states:
            next_space = (r + dr, c + dc)
            if next_space not in grid:
                continue
            new_heat = heat_so_far + grid[next_space]
            if new_heat >= best_so_far[next_space]:
                continue
            best_so_far[next_space] = new_heat
            if next_space == goal:
                final_best = min(final_best, new_heat)
                if debug:
                    print(final_best)
                continue
            potential_new_states = [(next_space, turn, 1, new_heat)
                                    for turn in get_turns(dr, dc)]
            if in_this_dir < 3:
                potential_new_states.append(
                    (next_space, (dr, dc), in_this_dir + 1, new_heat)
                )
            for x1, x2, x3, x4 in potential_new_states:
                if x4 < best_so_far[x1, x2, x3]:
                    best_so_far[x1, x2, x3] = x4
                    new_states.append((x1, x2, x3, x4))
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
