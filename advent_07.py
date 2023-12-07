# Part 1: 10:00, 101 (!); Part 2: 16:01, 101 (!!)
# Serves me right for reading all the intro text!  Anyway.  All the hard work
# is done in parse_data(); everything else in part_one/part_two is just "sort
# it and iterate over it".
from collections import Counter
from pathlib import Path

import aoc_util

TEST_CASE = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()


def parse_data(data, part=1):
    hands = []
    identifier = identify_hand if part == 1 else identify_hand_with_joker
    for line in data.splitlines():
        hand, bid = line.split()
        hands.append(
            (identifier(hand), hand_to_digits(hand, part=part), int(bid))
        )
    return hands


CARD_ORDER_ONE = '23456789TJQKA'
CARD_ORDER_TWO = 'J23456789TQKA'


def hand_to_digits(hand, part=1):
    # Turns a hand (string) into a tuple (of ints), so that hands will sort
    # based on strength
    order = CARD_ORDER_ONE if part == 1 else CARD_ORDER_TWO
    return [order.index(x) for x in hand]


def identify_hand(hand):
    count = sorted(Counter(hand).values())
    if count == [5]:
        return 6  # five of a kind
    if count == [1, 4]:
        return 5  # four of a kind
    if count == [2, 3]:
        return 4  # full house
    if count == [1, 1, 3]:
        return 3  # 3 of a kind
    if count == [1, 2, 2]:
        return 2  # two pair
    if count == [1, 1, 1, 2]:
        return 1  # one pair
    if count == [1, 1, 1, 1, 1]:
        return 0  # high card
    raise ValueError('Unknown hand')


def identify_hand_with_joker(hand):
    # Because there are no straights, you want to have as many of a single card
    # as possible.  That means jokers will always match whatever is most common
    # in the hand (and if there's a tie, it doesn't matter which).
    if hand == 'JJJJJ':
        return identify_hand(hand)
    most_common = Counter(hand.replace('J', '')).most_common()[0][0]
    return identify_hand(hand.replace('J', most_common))


def part_one(data=TEST_CASE, debug=False):
    hands = parse_data(data)
    hands.sort()
    total = 0
    for i, (_, _, bid) in enumerate(hands, start=1):
        total += i * bid
    return total


def part_two(data=TEST_CASE, debug=False):
    # ultimately, identical to part one except that the data is parsed by
    # "part 2" rules.
    hands = parse_data(data, part=2)
    hands.sort()
    total = 0
    for i, (_, _, bid) in enumerate(hands, start=1):
        total += i * bid
    return total


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
