#!/bin/python3

import sys
from collections import defaultdict

sys.setrecursionlimit(10000)

FILE = sys.argv[1] if len(sys.argv) > 1 else "17.in"


def horizontal_move(rock, state, movement):
    new_rock = [(r[0] + movement, r[1]) for r in rock]
    if all(
        ((r[1] not in state or r[0] not in state[r[1]]) and r[0] >= 0 and r[0] < 7)
        for r in new_rock
    ):
        return new_rock
    else:
        return rock


def drop_rock(highest, pattern, state, rock_index, jet_index):
    rocks = ["line", "cross", "L", "tower", "square"]

    rock_height = highest + 4

    # Left to right, top to bottom
    if rocks[rock_index] == "line":
        rock_coords = [
            (2, rock_height),
            (3, rock_height),
            (4, rock_height),
            (5, rock_height),
        ]
    elif rocks[rock_index] == "cross":
        rock_coords = [
            (3, rock_height + 2),
            (2, rock_height + 1),
            (3, rock_height + 1),
            (4, rock_height + 1),
            (3, rock_height),
        ]
    elif rocks[rock_index] == "L":
        rock_coords = [
            (4, rock_height + 2),
            (4, rock_height + 1),
            (2, rock_height),
            (3, rock_height),
            (4, rock_height),
        ]
    elif rocks[rock_index] == "tower":
        rock_coords = [
            (2, rock_height + 3),
            (2, rock_height + 2),
            (2, rock_height + 1),
            (2, rock_height),
        ]
    elif rocks[rock_index] == "square":
        rock_coords = [
            (2, rock_height + 1),
            (3, rock_height + 1),
            (2, rock_height),
            (3, rock_height),
        ]

    rock_index = (rock_index + 1) % len(rocks)

    while True:
        if pattern[jet_index] == "<":
            movement = -1
        else:
            movement = 1

        jet_index = (jet_index + 1) % len(pattern)
        rock_coords = horizontal_move(rock_coords, state, movement)
        down_rock = [(r[0], r[1] - 1) for r in rock_coords]

        if all( ((r[1] not in state or r[0] not in state[r[1]]) and r[1] > 0) for r in down_rock ):
            rock_coords = down_rock
        else:
            for r in rock_coords:
                state[r[1]].add(r[0])
            break

    return (rock_index, jet_index)


def solve(pattern, num_rocks=2022):
    rock_index = 0
    jet_index = 0
    highest = 0

    state = defaultdict(set)
    state_keys = dict()
    for curr in range(num_rocks):
        peak_sum = 0
        peaks = [0] * 7
        for k in state:
            vals = state[k]
            for v in vals:
                peaks[v] = max(peaks[v], k)
        peak_sum = tuple(highest - p for p in peaks)

        state_key = (rock_index, jet_index, peak_sum)
        if state_key in state_keys:
            print(len(state_keys), state_key)
            (prev_curr, prev_highest) = state_keys[state_key]
            cycle_period = curr - prev_curr
            remaining_cycles = (num_rocks - curr) // cycle_period
            remaining_iterations = num_rocks - (curr + cycle_period * remaining_cycles)
            x = (highest - prev_highest) * remaining_cycles
            print(cycle_period, prev_curr, curr, x)

            for _ in range(remaining_iterations):
                (rock_index, jet_index) = drop_rock(
                    highest, pattern, state, rock_index, jet_index
                )
                highest = max(state.keys())

            return highest + x

        else:
            state_keys[state_key] = (curr, highest)

        (rock_index, jet_index) = drop_rock(
            highest, pattern, state, rock_index, jet_index
        )

        highest = max(state.keys())
    return highest


def main():
    print(f"Using file {FILE}")
    with open(FILE, "r", encoding="utf-8") as f:
        pattern = []
        for line in f:
            line = list(line.strip())
            pattern.extend(line)

        print(f"Part one: {solve(pattern)}")
        print(f"Part two: {solve(pattern, num_rocks=1000000000000)}")


main()
