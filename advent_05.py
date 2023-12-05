# 712th after 45 minutes.  Hard one today!
# There's a lot to regret in the following code:
# * I think I kept wavering between representing a range as (first, last),
#   which is more natural, and (first, length), which is what the puzzle used.
#   Probably this would be easier to follow if I'd settled on one.
# * Obviously in the real world there wouldn't be a "parse_data_two", but
#   rather parse_data() would be updated to the genuinely better format, and
#   part_one() would be updated accordingly.
# * Honestly I didn't think the part_two() code was going to work the first
#   time.  (Technically the second, because I foolishly thought I could brute
#   force my way through the numbers, but the first in this incarnation.)

from pathlib import Path

import aoc_util

TEST_CASE = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".strip()


def parse_data(data):
    mappings = []
    seeds = None
    this_map = {}
    for line in data.splitlines():
        if not line:
            continue
        if line.startswith('seeds:'):
            seeds = [int(x) for x in line.split(': ')[1].split()]
        elif line.endswith(':'):
            this_map = {}
            mappings.append(this_map)
        else:
            dest, source, rangelen = [int(x) for x in line.split()]
            this_map[source] = (dest, rangelen)
    return seeds, mappings


def part_one(data=TEST_CASE, debug=False):
    seeds, mappings = parse_data(data)
    locations = set()
    for seed in seeds:
        # Taking it as given that the mappings are in order, we don't have to
        # care which mapping we're on: just take the output of one and use it
        # as the input of the next.
        for mapping in mappings:
            seed = apply_mapping(seed, mapping)
        locations.add(seed)
    return min(locations)


def apply_mapping(number, mapping):
    candidate_range = max([n for n in mapping if n < number], default=None)
    if candidate_range is None:
        return number
    dest, rangelen = mapping[candidate_range]
    if candidate_range <= number < candidate_range + rangelen:
        return dest + (number - candidate_range)
    return number


def parse_data_two(data):
    mappings = []
    seeds = None
    this_map = {}
    for line in data.splitlines():
        if not line:
            continue
        if line.startswith('seeds:'):
            seeds = [int(x) for x in line.split(': ')[1].split()]
        elif line.endswith(':'):
            this_map = {}
            mappings.append(this_map)
        else:
            dest, source, rangelen = [int(x) for x in line.split()]
            this_map[(source, source + rangelen)] = dest
    return seeds, mappings


def find_overlap(one, two):
    # Given two ranges, get the overlapping range, if any.
    s1, e1 = one
    s2, e2 = two
    if e1 <= s2 or e2 <= s1:
        return None
    return max(s1, s2), min(e1, e2)


def apply_mapping_to_ranges(seed_ranges, mapping):
    new_ranges = []
    for seed_start, size in seed_ranges:
        seed_end = seed_start + size
        overlaps_found = []

        # We don't know how broad the ranges are, and thus how many ranges in
        # the mapping they might overlap.  We could narrow that down by number,
        # but there aren't that many (and find_overlap() return None quickly
        # if there's no overlap), so just check them all.
        for cand_range, dest in mapping.items():
            overlap = find_overlap((seed_start, seed_end), cand_range)
            if overlap:
                o_start, o_end = overlap
                overlaps_found.append(
                    (o_start, o_end,
                     dest + o_start - cand_range[0], o_end - o_start)
                )
        overlaps_found.sort()

        # Now, for each overlap, add to the ranges:
        # * the range from the last endpoint to the overlap's starting point;
        #   this is a range not in the mapping and so is unmodified
        # * the overlap range, as modified to the corresponding dest range
        previous_end = seed_start
        for (o_start, o_end, new_start, new_size) in overlaps_found:
            new_ranges.append((previous_end, o_start - previous_end))
            new_ranges.append((new_start, new_size))
            previous_end = o_end
        new_ranges.append((previous_end, seed_end - previous_end))
    return [r for r in new_ranges if r[1]]


def part_two(data=TEST_CASE, debug=False):
    seeds, mappings = parse_data_two(data)
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))
    for mapping in mappings:
        seed_ranges = apply_mapping_to_ranges(seed_ranges, mapping)
    return min(seed_ranges)[0]


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    print(time.ctime(), part_one())
    print(time.ctime(), part_one(data=DATA))
    print(time.ctime(), part_two())
    print(time.ctime(), part_two(data=DATA))
