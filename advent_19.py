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


def get_function_for_condition(cond):
    comparitor, _, action = cond.rpartition(':')
    if not comparitor:
        return lambda x: action
    letter, comparitor, *number = comparitor
    number = int(''.join(number))
    if comparitor == '>':
        return lambda xmas: (action if xmas[letter] > number else False)
    if comparitor == '<':
        return lambda xmas: (action if xmas[letter] < number else False)
    raise ValueError(f'Unparseable: {cond}')


def parse_data(data):
    workflows, parts = data.split('\n\n')
    wf = {}
    for line in workflows.splitlines():
        name, condlist = line[:-1].split('{')
        conditions = []
        for cond in condlist.split(','):
            conditions.append(get_function_for_condition(cond))
        wf[name] = conditions
    pts = []
    for part in parts.splitlines():
        pt = re.match(r'\{'
                      r'x=(?P<x>\d+),'
                      r'm=(?P<m>\d+),'
                      r'a=(?P<a>\d+),'
                      r's=(?P<s>\d+)'
                      r'}', part).groupdict()
        pts.append({k: int(v) for k, v in pt.items()})
    return wf, pts


def evaluate_part(workflow, part):
    action = 'in'
    while True:
        conditions = workflow[action]
        for condition in conditions:
            new_action = condition(part)
            if new_action:
                break
        else:
            raise ValueError(f'Condition failed: {action}, {part}')
        if new_action in 'AR':
            return new_action
        action = new_action


def part_one(data=TEST_CASE, debug=False):
    total = 0
    workflow, parts = parse_data(data)
    for part in parts:
        if evaluate_part(workflow, part) == 'A':
            total += sum(part.values())
    return total


def part_two(data=TEST_CASE, debug=False):
    pass


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
