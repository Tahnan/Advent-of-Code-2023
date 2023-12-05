from pathlib import Path

import aoc_util

TEST_CASE = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip()


def part_one(data=TEST_CASE, debug=False):
    total = 0
    for line in data.splitlines():
        # Example:
        #  first.split() = [Card, 1:, 41, 48, 83, 86, 17]
        #  second.split() = [83, 86, 6, 31, 17, 9, 48, 53]
        # Obviously the first two things in first.split() are useless, but also
        # they're harmless, since they can't also appear in second.
        first, second = line.split(' | ')
        matches = len(set(first.split()) & set(second.split()))
        if matches:
            total += 2 ** (matches - 1)
    return total


def part_two(data=TEST_CASE, debug=False):
    # Just a little refactored from my original version, in which I first
    # iterated over the cards and created a list of the cards' values, and then
    # iterated over that list.  Might as well iterate once!
    data = data.splitlines()
    number_of_cards = {i: 1 for i in range(len(data))}
    for i, line in enumerate(data):
        first, second = line.split(' | ')
        card = len(set(first.split()) & set(second.split()))
        for j in range(card):
            number_of_cards[i + j + 1] += number_of_cards[i]
    # I forget what I did wrong the first time, but seeing the numbers helped.
    if debug:
        print(number_of_cards)
    return sum(number_of_cards.values())


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    print(time.ctime(), part_one())
    print(time.ctime(), part_one(data=DATA))
    print(time.ctime(), part_two(debug=True))
    print(time.ctime(), part_two(data=DATA))
