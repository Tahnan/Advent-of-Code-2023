# Day 10.  27:26 (1115), 01:14:44 (1068).  What a nightmare.
# My solution to part one seems reasonable enough; it just took me a long time
# to fumble through all the spacial reasoning.  Part two...I wonder if there
# was an easier way.  It took me a while to even sort through this one.

from collections import Counter

from grid_util import Grid
from pathlib import Path

import aoc_util

TEST_CASE_ONE = """
.....
.S-7.
.|.|.
.L-J.
.....
""".strip()

TEST_CASE_TWO = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""".strip()

# In Grid: first coord is N/S, second is E/W
CAN_MOVE_TO = {
    '|': ((-1, 0), (1, 0)),
    '-': ((0, -1), (0, 1)),
    'L': ((-1, 0), (0, 1)),
    'J': ((-1, 0), (0, -1)),
    '7': ((1, 0), (0, -1)),
    'F': ((1, 0), (0, 1)),
}

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def next_direction(dxdy, xy, grid):
    # If you just made a (dx, dy) move to (x, y), what's the next space you'll
    # be moving to?  Returns None if the move can't be made; (0, 0) if you've
    # moved to the start; and otherwise the direction from the cell that isn't
    # the one you just came from.

    # .get(), because xy might be outside the grid
    contents = grid.get(xy)
    if contents == 'S':
        return (0, 0)
    dx, dy = dxdy

    # .get(), because the contents might be None (from the .get() above), or
    # might be "." or some other non-pipe content.  Then the next move is the
    # only move from this cell that isn't the opposite of the dxdy move that
    # brought us *into* this cell; if there's not exactly one such move, return
    # None.
    can_move_to = CAN_MOVE_TO.get(contents, ())
    next_move = [pair for pair in can_move_to if pair != (-dx, -dy)]
    if len(next_move) == 1:
        return next_move[0]
    return None


def part_one(data, debug=False):
    grid = Grid.from_text(data)
    start, = [x for x, y in grid.items() if y == 'S']
    for dx, dy in DIRS:
        steps = 0
        x, y = start
        while True:
            neighbor = (x + dx, y + dy)
            next_move = next_direction((dx, dy), neighbor, grid)
            if not next_move:
                break
            steps += 1
            if grid[neighbor] == 'S':
                return steps / 2
            x, y = neighbor
            dx, dy = next_move
    raise RuntimeError('Fail!')


TEST_CASE_THREE = """
OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
""".strip()

TEST_CASE_FOUR = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip()


def part_two(data, debug=False):
    # Data-parsing more or less copied from part_one.  (When speed-coding, who
    # has time to refactor?)  Instead of counting steps, this stores the
    # loop coordinates in a set.
    grid = Grid.from_text(data)
    start, = [x for x, y in grid.items() if y == 'S']
    for orig_dx, orig_dy in DIRS:
        dx, dy = orig_dx, orig_dy
        x, y = start
        in_loop = {start}
        closed = False
        while not closed:
            neighbor = (x + dx, y + dy)
            next_move = next_direction((dx, dy), neighbor, grid)
            if not next_move:
                break
            if grid[neighbor] == 'S':
                closed = True
            else:
                in_loop.add(neighbor)
                x, y = neighbor
                dx, dy = next_move
        if closed:
            # A trick to replace "S" with the right shape: it's the one for
            # which the opposite of the move that brought us here is possible,
            # and also the original move is possible.
            grid[neighbor], = [
                shape for shape, dirs in CAN_MOVE_TO.items()
                if set(dirs) == {(orig_dx, orig_dy), (-dx, -dy)}
            ]
            break
    # now we have a complete set of everything in the loop, and we've replaced
    # "S" with the right shape.  So...
    for coord in grid:
        if coord not in in_loop:
            grid[coord] = '.'

    # Now replace every "." with I or O, based on the fact that an arbitrary
    # space on the grid has to cross an *even* number of lines to get to another
    # space with the same inside/outside status, and an *odd* number of lines
    # to get to one with the opposite status.
    #
    # Usually I use this logic in slitherlink-type puzzles, where the lines go
    # between the squares.  Here the lines are in the squares, so it took a
    # little bit of staring at the examples to work out what to do when faced
    # with a *parallel* line.  Answer: if you're looking at a perpendicular
    # line (in this case, "|", since I'm moving to the west), add one to the
    # number of lines crossed.  If you're looking at a *parallel* line, it has
    # to have a bend at both ends, and in that case: if one bend is one
    # direction and the other is the other, you've essentially crossed another
    # perpendicular line, and if they're in the same direction, you haven't.
    for space, contents in grid.items():
        if contents != '.':
            continue
        line_count = 0
        n_move = 0
        s_move = 0
        x, y = space
        while True:
            next_space = (x, y - 1)
            # If you've moved outside the grid, you're definitely in an outside
            # space!
            next_contents = grid.get(next_space, 'O')
            if next_contents in 'IO':
                # The even/odd logic described above.  We don't have to go all
                # the way to the edge of the grid, just to the next space to
                # the left whose status we already know.
                if line_count % 2:
                    grid[space] = 'I' if next_contents == 'O' else 'O'
                else:
                    grid[space] = next_contents
                break
            try:
                (x1, _), (x2, _) = CAN_MOVE_TO[next_contents]
            except KeyError:
                # Fortunately, even when my code went wrong I never hit this.
                # It's a RuntimeError because it only happens if my entire
                # logic is faulty.
                raise RuntimeError(f'Are we not going left to right? Status:'
                                   f' {space}, {next_space}, {next_contents}')
            # "|" will add one to n_move and one to s_move; "-" will add 0 to
            # both.  Otherwise, 1 is added to one direction but not the other.
            # If after all that there's 1 north move and one south move, we've
            # crossed a vertical line; if there's two moves in the same
            # direction, the counter can be reset and we haven't crossed one.
            n_move += 1 if -1 in (x1, x2) else 0
            s_move += 1 if 1 in (x1, x2) else 0
            n_move %= 2
            s_move %= 2
            if n_move and s_move:
                n_move = 0
                s_move = 0
                line_count += 1
            x, y = next_space
    if debug:
        # Really, *really* needed to see the output
        print(show_grid_with_box_drawing(grid.to_text(sep='')))

    return Counter(grid.values())['I']


def show_grid_with_box_drawing(data):
    # There are Unicode box-drawing characters for a reason, and this is that
    # reason.  So much easier to parse than the F/J/7/L nonsense.
    for a, b in (
        ('F', '┌'),
        ('7', '┐'),
        ('L', '└'),
        ('J', '┘'),
        ('|', '│'),
        ('-', '─')
    ):
        data = data.replace(a, b)
    return data


def show_the_grids():
    # Obviously a function used for debugging, i.e. "I am so lost, what am I
    # even looking at"
    for data in (TEST_CASE_ONE, TEST_CASE_TWO, TEST_CASE_THREE, TEST_CASE_FOUR):
        print(show_grid_with_box_drawing(data))


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    show_the_grids()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_one, {'data': TEST_CASE_ONE}),
        (part_one, {'data': TEST_CASE_TWO}),
        (part_one, {'data': DATA}),
        (part_two, {'data': TEST_CASE_THREE, 'debug': True}),
        (part_two, {'data': TEST_CASE_FOUR, 'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
