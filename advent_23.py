# Day 23, part one: 24:07 (868).  Mostly just some brute-forcing.
#
# I had a manager/tech lead named Moss Column (shoutout: hi, Moss!) whose answer
# to most design questions was "make an object".  Over time, I've found that
# he's not always right, but he's right at least more than I expected, if not
# more often than not.  So I decided to listen to my Inner Moss and use objects.
#
# I'n not sure it was right.  Well, it got me there.
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
ARROWS = ['^', '>', 'v', '<']


def parse_data(data):
    trails = Grid.from_text(data)
    rows = data.splitlines()
    start = (0, data.index('.'))
    end = (len(rows) - 1, rows[-1].index('.'))
    return trails, start, end


class State:
    # A state of traversal involves knowing:
    # * the current location;
    # * the previously-visited locations;
    # * the overall map.
    # And to distinguish part one from part two: whether the trails are
    # slippery, so that's also an initialization option.
    #
    # The goal is that the code will instantiate this exactly once, and each
    # state will generate subsequent states.  Which means there should probably
    # have been a classmethod for part_one() to use, but oh well.
    def __init__(self, current, trail_map, seen=None, slippery=True):
        self.current = current
        self.trail_map = trail_map
        self.seen = seen if seen else {current}
        self.slippery = slippery

    def step(self):
        next_steps = []
        try:
            if self.slippery:
                # I kind of like this trick: next directions are all four
                # cardinal directions, unless this is a slope, in which case
                # it's the element in DIRS corresponding to this slope's
                # element in ARROWS.  Of course, by the light of day, it seems
                # like a dict would have been better....
                current_arrow = ARROWS.index(self.trail_map[self.current])
                next_dirs = [DIRS[current_arrow]]
            else:
                next_dirs = DIRS
        except ValueError:
            # Why is this a try/except?  Um...good question.
            next_dirs = DIRS
        r, c = self.current
        for dr, dc in next_dirs:
            next_space = (r + dr, c + dc)
            if (next_space in self.seen
                or self.trail_map.get(next_space, '#') == '#'):
                continue
            next_steps.append(self._clone(next_space))
        return next_steps

    def _clone(self, next_space):
        # Return a new state based on this state, but for the next space
        return State(next_space, self.trail_map, self.seen | {next_space},
                     slippery=self.slippery)

    def path_length_if_done(self, end):
        if self.current == end:
            return len(self.seen) - 1  # Because "start" isn't a step

    def __repr__(self):
        # Probably not a proper __repr__ per the Python documentation, but it's
        # what I needed for debugging purposes
        return f'State(current={self.current}, seen={len(self.seen)})'


def part_one(data=TEST_CASE, slippery=True, debug=False):
    trails, start, end = parse_data(data)
    current_states = [State(start, trails, slippery=slippery)]
    longest_path = 0
    longest_new_states = 0
    while current_states:
        new_states = []
        for state in current_states:
            # As promised in the comment on State: the start State is generated
            # above, and now we use state.step() to get subsequent states
            for next_state in state.step():
                path = next_state.path_length_if_done(end)
                if path:
                    longest_path = max(longest_path, path)
                else:
                    new_states.append(next_state)
        if debug and longest_new_states < len(new_states):
            longest_new_states = len(new_states)
            print(longest_path, len(new_states))
        current_states = new_states
    return longest_path


def part_two(data=TEST_CASE, debug=False):
    # In fact, this takes impossibly long; see next file.
    return part_one(data=data, debug=debug, slippery=False)


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
        (part_two, {'data': DATA, 'debug': True}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
