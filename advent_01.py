from pathlib import Path

TEST_CASE = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".strip()

TEST_CASE_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    pass


def part_one(data=TEST_CASE, debug=False):
    total = 0
    for line in data.splitlines():
        digits = [x for x in line if x.isdigit()]
        total += 10 * int(digits[0]) + int(digits[-1])
    return total


DIGITS = [str(x) for x in range(10)] + [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine'
]


def part_two(data=TEST_CASE_2, debug=False):
    # This feels so kludgy!  It works, but still.
    total = 0
    for line in data.splitlines():
        left_digit = None
        right_digit = None
        left_digit_loc = 999  # that had better be longer than any line
        right_digit_loc = -1
        for i, digit in enumerate(DIGITS):
            if digit not in line:
                continue
            lloc = line.find(digit)
            if lloc < left_digit_loc:
                left_digit_loc = lloc
                left_digit = i % 10
            rloc = line.rfind(digit)
            if rloc > right_digit_loc:
                right_digit_loc = rloc
                right_digit = i % 10
        total += 10 * left_digit + right_digit
    return total


def better_part_two(data):
    # Instead of the above, let's preprocess the data by inserting digits
    # where the spelled-out forms are.  Not in place of them, because of cases
    # like "eightwo"!
    for spelled, digited in (
        ('one', 'on1e'),
        ('two', 'tw2o'),
        ('three', 'thr3ee'),
        ('four', 'fo4ur'),
        ('five', 'fi5ve'),
        ('six', 'si6x'),
        ('seven', 'se7en'),
        ('eight', 'ei8ht'),
        ('nine', 'ni9ne'),
        ('zero', 'ze0ro')
    ):
        data = data.replace(spelled, digited)
    return part_one(data=data)


if __name__ == '__main__':
    import time
    name = Path(__file__).name.replace('advent', 'input').replace('py', 'txt')
    data_path = Path(__file__).with_name(name).absolute()
    if data_path.exists():
        with data_path.open() as f:
            DATA = f.read()
    else:
        DATA = ''

    print(time.ctime(), 'Start')
    print(time.ctime(), part_one())
    print(time.ctime(), part_one(data=DATA))
    print(time.ctime(), part_two())
    print(time.ctime(), part_two(data=DATA))
    print(time.ctime(), better_part_two(DATA))
