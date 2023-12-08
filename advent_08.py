# Day 8.  Part 1: 5:17, 487th.  Part 2: 25:12, 1195th.
#
# I hate traversing graphs.
#
# Yes, I tried to brute force part 2.  Yes, I realized why that wouldn't work
# and how to do it right, and then I screwed that up for a bit, and eventually
# I ended up with the code below, which gave me:
#
#    [{'ZZZ': [17263, 34526]}, ...]
#
# Then I went into ipython and confirmed several things:
# * There was only one Z-node that each path passed through.  (That certainly
#   wasn't a given.)
# * For all of the paths, the Z-node was hit after N moves, and then after 2N
#   moves.  (Also very much not a given; they could hit the Z-node multiple
#   times at different intervals, they could loop back to the middle of their
#   paths, etc.  But they did not.)
#
# At that point, the answer was just math.lcm(*steps), where "steps" was the
# length of the cycle for each Z-node.  Really expected that the math wasn't
# going to be so straightforward, which was why I printed the cycles: I thought
# I was just spot-checking my state, not skipping the rest of the code.)
#
# Ah well.

import itertools
from pathlib import Path

import aoc_util

TEST_CASE = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip()

SECOND_TEST_CASE = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    lr, nodes = data.split('\n\n')
    node_map = {}
    for line in nodes.splitlines():
        start, rest = line.split(' = ')
        rest = rest.strip('()').split(', ')
        node_map[start] = dict(zip('LR', rest))
    return lr, node_map


def part_one(data=TEST_CASE, debug=False):
    steps = 0
    lr, node_map = parse_data(data)
    current = 'AAA'
    directions = itertools.cycle(lr)
    for d in directions:
        steps += 1
        current = node_map[current][d]
        if current == 'ZZZ':
            return steps


def part_two(data=SECOND_TEST_CASE, debug=False):
    lr, node_map = parse_data(data)
    current_nodes = [node for node in node_map if node.endswith('A')]
    cycles = []
    for node in current_nodes:
        steps = 0
        endpoints = {}
        seen_states = {(node, 0)}
        for i, d in itertools.cycle(enumerate(lr)):
            steps += 1
            node = node_map[node][d]
            if node.endswith('Z'):
                endpoints.setdefault(node, []).append(steps)
                if (node, i) in seen_states:
                    break
            seen_states.add((node, i))
        cycles.append(endpoints)
    return cycles


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    one_a = part_one()
    print(time.ctime(), one_a)
    one_b = part_one(data=DATA)
    print(time.ctime(), one_b)
    two_a = part_two()
    print(time.ctime(), two_a)
    two_b = part_two(data=DATA, debug=True)
    print(time.ctime(), two_b)
