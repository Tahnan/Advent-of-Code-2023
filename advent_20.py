# Part one.  Time not included (mostly because I was feeling feverish at
# 12:30am and went to bed rather than finish, so I resumed mid-afternoon).
#
# Objects seemed the way to go this time.  Possibly overkill, I don't know.
# There's also a little code for checking states and looking for loops, because
# the instructions seemed to suggest that would be part of the task, but it
# wasn't helpful for part 1 and clearly wouldn't be helpful for part 2.
#
# Pushing this now because I don't know if I'll ever get to part two, which
# looks to be less "coding" and more "analyzing the input".
from collections import Counter
from pathlib import Path

import aoc_util

TEST_CASE = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".strip()

TEST_CASE_TWO = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""".strip()


class Button:
    # The button sets everything up: parses the data, creates modules, tracks
    # them, passes around signals, etc.
    def __init__(self, data):
        # Things to track include the number of high and low pulses sent, and
        # the pulses waiting to be processed.
        self.sent_memory = Counter()
        self.pulse_queue = []

        # First create the modules (broadcast, conjunction, and flipflop)...
        self.modules = {}
        for line in data.splitlines():
            module_name, _ = line.split(' -> ')
            if module_name == 'broadcaster':
                self.modules[module_name] = Broadcast()
            elif module_name.startswith('&'):
                self.modules[module_name[1:]] = Conjunction()
            elif module_name.startswith('%'):
                self.modules[module_name[1:]] = FlipFlop()
            else:
                raise ValueError(f'Unknown module: {line}')

        # ...then store the destinations for each module--this is done after,
        # so that if any modules are non-existent destinations, we can set up
        # dummy Modules for them...
        self.destinations = {}
        for line in data.splitlines():
            module_name, destinations = line.split(' -> ')
            dest_names = destinations.split(', ')
            module_name = (module_name if module_name == 'broadcaster'
                           else module_name[1:])
            self.destinations[module_name] = dest_names
            for name in dest_names:
                if name not in self.modules:
                    self.modules[name] = Module()

        # ...and once we know everything's destination modules, we can work out
        # everything's *input* modules, and tell each module what they are
        # (only the Conjunction modules care, but it's easier to just tell all
        # of them).
        for module_name, module in self.modules.items():
            input_modules = [x for x, y in self.destinations.items()
                             if module_name in y]
            module.set_inputs(input_modules)

    def get_states(self):
        return tuple([mod.report_state() for _, mod in self.modules.items()])

    def press_button(self, debug=False):
        # When the button is pressed, it sends a "low" pulse to the broadcaster,
        # and then handles each pulse in the queue unmtil the queue is empty.
        self.pulse_queue.append(('button', 'broadcaster', 'low'))
        while self.pulse_queue:
            source, destination, pulse = self.pulse_queue.pop(0)
            if debug:
                # The format used in the problem
                print(f'{source} -{pulse}-> {destination} | {self.sent_memory}')
            self.sent_memory[pulse] += 1

            # Find the pulse to send, *if any* (in some cases no action is
            # taken!), and add the source/destination/pulse to the queue for
            # each of the module's destinations
            to_send = self.modules[destination].receive(source, pulse)
            if to_send:
                self.pulse_queue.extend(
                    [(destination, d, to_send)
                     for d in self.destinations[destination]]
                )

        # Return the counter of pulses sent, and the current states of things
        pulses_sent = dict(self.sent_memory)
        self.sent_memory.clear()
        return self.get_states(), pulses_sent


class Module:
    # Base module; also instantiable for "untyped modules" (like "output" in
    # the example).
    def __init__(self):
        self.memory = {}

    def receive(self, source, pulse):
        # for dummy modules, do nothing
        pass

    def set_inputs(self, input_modules):
        # Only needed for the Conjunction, but easlier this way
        self.memory.update({im: 'low' for im in input_modules})

    def report_state(self):
        return None


class Broadcast(Module):
    # The only thing a broadcast module does is send out what it receives.
    def receive(self, source, pulse):
        return pulse


class FlipFlop(Module):
    def __init__(self):
        super().__init__()
        self.current_state = 'off'

    def receive(self, source, pulse):
        if pulse == 'high':
            return
        if self.current_state == 'off':
            self.current_state = 'on'
            return 'high'
        else:
            self.current_state = 'off'
            return 'low'

    def report_state(self):
        return self.current_state


class Conjunction(Module):
    def receive(self, source, pulse):
        self.memory[source] = pulse
        return 'low' if set(self.memory.values()) == {'high'} else 'high'

    def report_state(self):
        return '/'.join(pulse for _, pulse in sorted(self.memory.items()))


def part_one(data=TEST_CASE, presses=1000, debug=False):
    button = Button(data)
    # Code for tracking states; see comment at top
    #
    # seen_states = {button.get_states(): (-1, Counter())}
    # for i in range(presses):
    #     states, pulses_sent = button.press_button(debug=debug)
    #     if states in seen_states:
    #         break
    #     seen_states[states] = (i, pulses_sent)
    # return i
    pulses = Counter()
    for _ in range(presses):
        _, pulses_sent = button.press_button(debug=debug)
        pulses += pulses_sent
    return pulses['low'] * pulses['high']


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
        (part_one, {'debug': True, 'presses': 1}),
        (part_one, {'data': TEST_CASE_TWO}),
        (part_one, {'data': DATA}),
        (part_two, {'data': DATA}),
    ):
        result = fn(**kwargs)
        print(time.ctime(), result)
