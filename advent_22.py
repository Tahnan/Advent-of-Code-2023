# Day 22: 26:08 (190), 40:33 (332).  That felt better.
from pathlib import Path

import aoc_util

TEST_CASE = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""".strip()


def parse_data(data):
    space = {}
    bricks_to_coords = {}
    for i, line in enumerate(data.splitlines()):
        bricks_to_coords[i] = set()
        one, two = line.split('~')
        x_one, y_one, z_one = [int(c) for c in one.split(',')]
        x_two, y_two, z_two = [int(c) for c in two.split(',')]
        # They're all 1x1xN, so two of these ranges cover a single number, but
        # this is much easier than working out *which* coordinate varies
        for x in range(min(x_one, x_two), max(x_one, x_two) + 1):
            for y in range(min(y_one, y_two), max(y_one, y_two) + 1):
                for z in range(min(z_one, z_two), max(z_one, z_two) + 1):
                    space[(x, y, z)] = i
                    bricks_to_coords[i].add((x, y, z))
    return space, bricks_to_coords


def get_neighboring_bricks(data):
    # Both part one and part two depend solely on which bricks are supporting
    # which others (and vice versa), so this function parses the data, drops the
    # bricks, and returns that information as two dictionaries.
    # If you thought I had this factored out before I did part two: aww, that's
    # so sweet of you!  (In fact, this was all in part_one(), and then I added
    # a "part=1" keyword argument to it that, if set to "2", would return the
    # two dicts.  Hack hack hack but at least it worked.)
    space, brick_locations = parse_data(data)

    # first, drop the bricks
    bricks_that_can_drop = set(space.values())
    while bricks_that_can_drop:
        cannot_drop = set()
        for brick in bricks_that_can_drop:
            spaces_below = {(x, y, z - 1) for x, y, z in brick_locations[brick]}
            if any(z == 0 for x, y, z in spaces_below):
                # It's on the ground; it's not going anywhere
                cannot_drop.add(brick)
                continue
            # Find out what's below it other than empty space or other cubes in
            # the same brick
            contents_below = {space.get(coord) for coord in spaces_below}
            contents_below -= {None, brick}
            if not contents_below:
                # If there's nothing below it, drop it and update its location;
                # consider it still a candidate for falling further
                for loc in brick_locations[brick]:
                    del space[loc]
                for loc in spaces_below:
                    space[loc] = brick
                brick_locations[brick] = spaces_below
            elif not (contents_below & bricks_that_can_drop):
                # None of the bricks below can drop, so neither can this one
                cannot_drop.add(brick)
        bricks_that_can_drop -= cannot_drop

    # Now that they've fallen, find out which bricks each brick supports (i.e.
    # bricks_above) and which bricks each brick rests on (i.e., bricks_below)
    bricks_above = {}
    bricks_below = {}
    for brick, locations in brick_locations.items():
        below = {space.get((x, y, z - 1)) for x, y, z in locations}
        below -= {None, brick}  # As above: ignore space/ground and itself
        bricks_below[brick] = below
        above = {space.get((x, y, z + 1)) for x, y, z in locations}
        above -= {None, brick}
        bricks_above[brick] = above
    return bricks_above, bricks_below


def part_one(data=TEST_CASE, debug=False):
    bricks_above, bricks_below = get_neighboring_bricks(data)
    can_disintegrate = 0
    for brick, above in bricks_above.items():
        if all(len(bricks_below[b]) > 1 for b in above):
            can_disintegrate += 1
    return can_disintegrate


def part_two(data=TEST_CASE, debug=False):
    bricks_above, bricks_below = get_neighboring_bricks(data)
    will_fall = 0
    for brick in bricks_above:
        # Something in here might be overkill--I'm not sure that I need to keep
        # checking bricks on top of previously-fallen bricks--but the time is
        # negligible compared to the time it would take me to visualize this.
        will_fall_now = {brick}
        more_will_fall = True
        while more_will_fall:
            more_will_fall = set()
            for wfn in will_fall_now:
                above = bricks_above[wfn]
                for may_fall_now in above:
                    if bricks_below[may_fall_now].issubset(will_fall_now):
                        more_will_fall.add(may_fall_now)
            more_will_fall -= will_fall_now
            will_fall_now |= more_will_fall
        will_fall += len(will_fall_now) - 1
    return will_fall


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
