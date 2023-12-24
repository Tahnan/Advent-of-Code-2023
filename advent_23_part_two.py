# Day 23, part two: 23:14:23 (9014).  Hard to believe I spent 23 uninterrupted
# hours working on this!
#
# The test data ran fine in the brute-force method of part one, but that wasn't
# going to work out well here.  I realized I could reduce the map to just its
# junctions--hey, anyone else tired of finding paths through graphs?--and that
# also was taking too long, until I put in the "don't walk past the exit" check.
from pathlib import Path

import aoc_util
from grid_util import Grid

TEST_CASE = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""".strip()


DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_data(data):
    trails = Grid.from_text(data)
    rows = data.splitlines()
    start = (0, data.index('.'))
    end = (len(rows) - 1, rows[-1].index('.'))
    return trails, start, end


def map_reduce(trail_map, start, end):
    # Because we're reducing the size of the trail map.  I vaguely feel like
    # "map reduce" might already mean something in programming?  Whatever.

    # First, find the junctions.  For each one, store a mapping from the
    # directions of its exits to--for now--"None", which we can use later as a
    # check for "have we already worked this one out".
    junctions = {start: {(1, 0): None}, end: {(-1, 0): None}}
    for (r, c), contents in trail_map.items():
        if (r, c) == start or (r, c) == end:
            continue
        if contents != '#':
            neighbors = [trail_map[(r + dr, c + dc)] for dr, dc in DIRS]
            if neighbors.count('#') >= 2:
                continue
            junctions[(r, c)] = {
                direction: None for direction, neighbor in zip(DIRS, neighbors)
                if neighbor != '#'
            }

    # Then, for each junction, walk the path to the next one, and record where
    # you end up (and add the reverse walk as well)
    for (r, c), directions in junctions.items():
        for (dr, dc), path in directions.items():
            if path:
                # Then we hit this from the opposite direction
                continue
            steps = 1
            current_r = r + dr
            current_c = c + dc
            # The next step is either forward, left, or right (don't just check
            # all of DIRS because then we have to work to leave out the space
            # we came from, and bleh.
            next_directions = [(dr, dc), (-dc, dr), (dc, -dr)]
            while (current_r, current_c) not in junctions:
                steps += 1
                (next_dr, next_dc), = [
                    (ndr, ndc) for ndr, ndc in next_directions
                    if trail_map[(current_r + ndr, current_c + ndc)] != '#'
                ]  # We're not at a junction; there must only be one
                next_directions = [
                    (next_dr, next_dc),
                    (-next_dc, next_dr),
                    (next_dc, -next_dr)
                ]
                current_r += next_dr
                current_c += next_dc
            directions[(dr, dc)] = ((current_r, current_c), steps)
            junctions[(current_r, current_c)][(-next_dr, -next_dc)] = ((r, c), steps)

    junctions = {coord: list(directions.values())
                 for coord, directions in junctions.items()}

    # One more adjustment: there's no point in going through the junction that
    # leads to the exit unless you're going to the exit, so fold that in.
    (pre_exit, pre_exit_steps), = junctions[end]
    lead_to_exit = junctions.pop(pre_exit)
    for pre_pre_exit, steps in lead_to_exit:
        junctions[pre_pre_exit].remove((pre_exit, steps))
        junctions[pre_pre_exit].append((end, steps + pre_exit_steps))
    return junctions


def part_two(data=TEST_CASE, debug=False):
    trail_map, start, end = parse_data(data)
    junctions = map_reduce(trail_map, start, end)
    states = [(start, {start}, 0)]
    longest_path = 0
    longest_states = 0
    while states:
        new_states = []
        for (location, seen, steps) in states:
            for (next_location, more_steps) in junctions[location]:
                if next_location in seen:
                    continue
                new_steps = steps + more_steps
                if next_location == end:
                    longest_path = max(longest_path, new_steps)
                    continue
                new_states.append(
                    (next_location, seen | {next_location}, new_steps)
                )
        states = new_states
        if debug and len(states) > longest_states:
            longest_states = len(states)
            print(longest_path, longest_states)
    return longest_path


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_two, {'debug': True}),
        (part_two, {'debug': True, 'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
