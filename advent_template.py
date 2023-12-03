from pathlib import Path

TEST_CASE = """
""".strip()


def parse_data(data):
    # pre-defined in case it's needed
    pass


def part_one(data=TEST_CASE, debug=False):
    pass


def part_two(data=TEST_CASE, debug=False):
    pass


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
