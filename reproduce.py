"""Reproduce the seeded tournament recorded in Cairn fact f001."""

import random

from pig import hold_at_ten, hold_at_twenty, run_tournament


if __name__ == "__main__":
    random.seed(20261028)
    wins = run_tournament(hold_at_twenty, hold_at_ten, games=10000)
    print(f"Exact hold-at-20 win rate: {wins[0] / 10000:.2%}")
    if wins != [6983, 3017]:
        raise SystemExit("Totals differ from the recorded experiment; investigate before reporting a match.")
    print("Recorded result reproduced: the 55% goal is met.")
