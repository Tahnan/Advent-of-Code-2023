# Day 19, part two.  Different enough from part one that it gets its own file.
# Part one: 44:46 (3042); part two, 01:21:09 (1522).
#
# Remember the other day when we had to track ranges of seeds, and not all the
# individual numbers in those ranges?  Welcome back to that.
import re
from pathlib import Path

import aoc_util

TEST_CASE = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".strip()


def parse_data(data):
    # Just like Part One, but we don't care about the "parts" half
    workflows, parts = data.split('\n\n')
    wf = {}
    for line in workflows.splitlines():
        name, condlist = line[:-1].split('{')
        conditions = []
        for cond in condlist.split(','):
            comparitor, _, action = cond.rpartition(':')
            if comparitor:
                letter, comparitor, *number = comparitor
                number = int(''.join(number))
            else:
                letter, comparitor, number = '', '', ''
            conditions.append((letter, comparitor, number, action))
        wf[name] = conditions
    return wf


def trace_states(xmas, workflow, condition_list, debug=False):
    # "xmas" here is a dictionary from 'x, m, a, s' to ranges--initially
    # (1, 4000), but those narrow as we go.
    #
    # "pass" and "fail" below mean not accept/reject, but rather "pass/fail
    # the current condition".

    # If any range is invalid, there are no Accept states in its future.
    if any(start > end for start, end in xmas.values()):
        return 0
    (letter, comparitor, number, action), *remaining = condition_list
    if letter:
        # If this is a non-default condition, split into two cases:
        # * pass_xmas, which is like xmas but only for the part of the range
        #   that passes the condition;
        # * fail_xmas, which is the rest of the range
        start, end = xmas[letter]
        pass_xmas = {**xmas, letter: ((start, number - 1) if comparitor == '<'
                                      else (number + 1, end))}
        fail_xmas = {**xmas, letter: ((start, number) if comparitor == '>'
                                      else (number, end))}
    else:
        # And if this is a default condition, everything in the xmas ranges
        # passes it
        pass_xmas = xmas
        fail_xmas = None

    # "action" is the action to take if the condition passes.  If that action
    # is "R", then nothing passes; if it's "A", then everything in the range
    # passes (which, in standard combinatorics fashion, is the product of the
    # options: number of x values in the range times number of m values etc.
    # And if it's another state, then we call this function again with the new
    # pass_xmas range and that state's workflow as the action list.
    if action == 'R':
        pass_number = 0
    elif action == 'A':
        pass_number = 1
        for start, end in pass_xmas.values():
            pass_number *= (end - start + 1) if end >= start else 0
    else:
        pass_number = trace_states(pass_xmas, workflow, workflow[action],
                                   debug=debug)
    # Conversely: if nothing fails (e.g. because we're in a default value),
    # then there's no fail_xmas ranges; otherwise, anything that fails goes on
    # to the next condition in the current workflow, and we call this function
    # again with the new fail_xmas range and the remaining conditions.
    if fail_xmas:
        fail_number = trace_states(fail_xmas, workflow, remaining, debug=debug)
    else:
        fail_number = 0
    return pass_number + fail_number


def part_two(data=TEST_CASE, debug=False):
    workflow = parse_data(data)
    xmas = {letter: (1, 4000) for letter in 'xmas'}
    return trace_states(xmas, workflow, workflow['in'], debug=debug)


if __name__ == '__main__':
    import time
    day = Path(__file__).name[7:9]
    input_file = aoc_util.get_input_file(day)
    with input_file.open() as f:
        DATA = f.read()

    print(time.ctime(), 'Start')
    for fn, kwargs in (
        (part_two, {'debug': True}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
