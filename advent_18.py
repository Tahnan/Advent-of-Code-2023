# Day 18.  Well, that was a disaster.
#
# Part one was easy enough (17:22, 597).  Then I stalled entirely on part two,
# eventually looked up the formula for the area of a polygon based on its
# coordinates, realized that everything was off by one, spent some time working
# through that, finally decided the easiest way to handle that was to consider
# the coordinates as the center of each pit (so that (0, 0) to (0, 6) would
# be six units long, even though the side was seven units long); calculate the
# area; add half the perimeter to represent the fact that each line of the
# polygon had a half square along its exterior; and then add in a correction
# for the vertices.
#
# The vertices went badly.  Each one adds a quarter square, *unless* it bends
# the *other* way, in which case it *subtracts* a (double-counded) quarter
# square.  I think.  I never got it right.  I ran it, it did the right thing
# for the example and for part one, and for part two it...gave me a number
# ending in ".5".
#
# I rounded up, and was wrong (my guess was too high).  I reversed the input,
# in case that helped, and I got a whole number, but it was too low.  But since
# I was *close*, those two numbers were two apart, which pretty much gave me
# the answer, and I decided to take it.
#
# I hate geometry.
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""".strip()

DIRS = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}


def parse_data(data):
    plan = []
    for line in data.splitlines():
        d, n, code = line.split()
        plan.append((d, int(n), code[2:-1]))
    return plan


def parse_part_two(data):
    return [
        ('RDLU'[int(hexcode[-1])], int(hexcode[:-1], 16), None)
        for _, _, hexcode in parse_data(data)
    ]


def get_grid_from_plan(plan):
    spaces = {(0, 0)}
    r, c = 0, 0
    for direction, distance, _ in plan:
        dr, dc = DIRS[direction]
        for _ in range(distance):
            r += dr
            c += dc
            spaces.add((r, c))
    min_r, min_c = [min(dim) for dim in zip(*spaces)]
    spaces = {(r - min_r, c - min_c) for r, c in spaces}
    max_r, max_c = [max(dim) for dim in zip(*spaces)]
    grid = Grid.from_dimensions(max_r + 1, max_c + 1, default='_')
    for space in spaces:
        grid[space] = '#'
    return grid


def floodfill(grid):
    space = (0, 0)
    while grid[space] != '#':
        space = (space[0] + 1, 0)
    space = (space[0] + 1, 0)
    while grid[space] != '_':
        space = (space[0], space[1] + 1)
    spread_from = {space}
    while spread_from:
        new_spread = set()
        for r, c in spread_from:
            grid[(r, c)] = '#'
            for dr, dc in DIRS.values():
                neighbor = (r + dr, c + dc)
                if grid.get(neighbor) == '_':
                    new_spread.add(neighbor)
        spread_from = new_spread


def area_of_a_polygon(endpoints):
    area = 0
    for (x1, y1), (x2, y2) in zip(endpoints, endpoints[1:] + [endpoints[0]]):
        new_val = (x1 * y2) - (x2 * y1)
        area += new_val
    return abs(area // 2)


def part_one(data=TEST_CASE, debug=False):
    plan = parse_data(data)
    grid = get_grid_from_plan(plan)
    if debug:
        print(grid.to_text(), end='\n\n')
    floodfill(grid)
    if debug:
        print(grid.to_text())
    return sum(c == '#' for c in grid.values())


def alt_part_one(data=TEST_CASE, debug=False):
    plan = parse_data(data)
    x, y = (0, 0)
    points = [(0, 0)]
    perimeter = 0
    vertex_adjustment = 0
    last_dxdy = DIRS[plan[-1][0]]

    dx, dy = DIRS[plan[0][0]]
    if last_dxdy == (-dy, dx):
        def adjustment(dx, dy, last_dxdy):
            return .25 * (1 if (-dy, dx) == last_dxdy else -1)
    else:
        def adjustment(dx, dy, last_dxdy):
            return .25 * (1 if (dy, -dx) == last_dxdy else -1)
    for direction, distance, _ in plan:
        dx, dy = DIRS[direction]
        x += dx * distance
        y += dy * distance
        points.append((x, y))
        perimeter += distance
        vertex_adjustment += adjustment(dx, dy, last_dxdy)
        last_dxdy = (dx, dy)
    if debug:
        print(points)
        print('Area:', area_of_a_polygon(points))
        print('Perimeter / 2:', perimeter / 2)
        print('Vertex adjustment:', vertex_adjustment)
    return area_of_a_polygon(points) + perimeter / 2 + vertex_adjustment


def part_two(data=TEST_CASE, debug=False):
    plan = parse_part_two(data)
    x, y = (0, 0)
    points = [(0, 0)]
    perimeter = 0
    vertex_adjustment = 0
    first_dx, first_dy = DIRS[plan[0][0]]
    last_dxdy = (-first_dy, first_dx)
    for direction, distance, _ in plan:
        dx, dy = DIRS[direction]
        x += dx * distance
        y += dy * distance
        points.append((x, y))
        perimeter += distance
        vertex_adjustment += .25 * (1 if (-dy, dx) == last_dxdy else -1)
        last_dxdy = (dx, dy)
    if debug:
        print(points)
        print('Area:', area_of_a_polygon(points))
        print('Perimeter / 2:', perimeter / 2)
        print('Vertex adjustment:', vertex_adjustment)
    return area_of_a_polygon(points) + perimeter / 2 + vertex_adjustment


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'debug': True}),
        (alt_part_one, {'debug': True}),
        (part_one, {'data': DATA}),
        (alt_part_one, {'data': DATA}),
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
