from pathlib import Path
import aoc_util

TEST_CASE = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()


# RGB order
def parse_data(data):
    # pre-defined in case it's needed
    lines = []
    for line in data.splitlines():
        _, num, rounds = line.split(' ', 2)
        num = int(num.strip(':'))
        rgbs = []
        for round in rounds.split('; '):
            colors = round.split(', ')
            rgb = [0, 0, 0]
            for c in colors:
                n, clr = c.split()
                rgb[('red', 'green', 'blue').index(clr)] += int(n)
            rgbs.append(rgb)
        lines.append((num, rgbs))
    return lines


def part_one(data=TEST_CASE, debug=False):
    game_sum = 0
    for num, rounds in parse_data(data):
        for round in rounds:
            r, g, b = round
            if r > 12 or g > 13 or b > 14:
                break
        else:
            game_sum += num
    return game_sum


def part_two(data=TEST_CASE, debug=False):
    powers = 0
    for _, rounds in parse_data(data):
        rs, gs, bs = zip(*rounds)
        powers += max(rs) * max(gs) * max(bs)
    return powers


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
