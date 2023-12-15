# Day 15: 3:23 (479), 12:34 (173)
#
# The hardest part honestly was just reading the instructions.  The *easiest*
# part was using Python, because its dictionaries are ordered, so all of the
# tracking of "remove the lens and move everything else forward without
# changing the order" was already handled.  It felt like cheating, but hey, I'm
# not *forcing* anyone to use Java.  (What am I, a monster?)

from pathlib import Path

import aoc_util

TEST_CASE = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""".strip()


def hash_algorithm(string):
    current = 0
    for symbol in string:
        current = ((current + ord(symbol)) * 17) % 256
    return current


def part_one(data=TEST_CASE, debug=False):
    total = 0
    for piece in data.replace('\n', '').split(','):
        total += hash_algorithm(piece)
    return total


def part_two(data=TEST_CASE, debug=False):
    boxes = {i: {} for i in range(256)}
    for piece in data.replace('\n', '').split(','):
        if piece.endswith('-'):
            label = piece[:-1]
            boxes[hash_algorithm(label)].pop(label, None)
        elif '=' in piece:
            label, focal_length = piece.split('=')
            boxes[hash_algorithm(label)][label] = int(focal_length)

    focal_power = 0
    for box, contents in boxes.items():
        for slot, (_, length) in enumerate(contents.items(), start=1):
            focal_power += (box + 1) * slot * length
    return focal_power


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
