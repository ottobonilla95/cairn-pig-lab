# Experiment results and conclusion

## Objective

Find a rule for when to stop rolling in Pig that wins at least 55% of 10,000 games
against an opponent that always holds at 10 turn points. Players race to 100 banked
points. The engine forces an immediate bank when a winning total is reached.

## Recorded measurement

| Item | Value |
| --- | --- |
| Run date | 28 October 2026 |
| Cairn project | `proj_001`, Pig strategy test |
| Candidate | `hold_at_twenty`: hold at 20 or more turn points |
| Baseline | `hold_at_ten`: hold at 10 or more turn points |
| Games | 10,000 |
| Starts | 5,000 per strategy, alternating starting positions |
| Random seed | `20261028` |
| Candidate wins | 6,983 |
| Baseline wins | 3,017 |
| Candidate win rate | **69.83%** |
| Required win rate | 55% |
| Margin above target | 14.83 percentage points |
| Project status | Completed |

The run used Python's seeded pseudorandom generator. A separate local reproduction
of the worker's command produced the same totals, using the unchanged simulator.
This reproduction was performed after the worker completed; it was not another
Cairn worker's verification task.

## Agent trace

1. The user created the project through Cairn's dashboard with bootstrap enabled.
2. The dispatcher was launched with `cairn dispatch --config dispatch.yaml --once`.
3. `worker-a` claimed intent `i001`, the bootstrap task, at 00:57:26 UTC.
4. It ran the existing hold-at-20 strategy against hold-at-10 in 10,000 games.
5. It recorded the measurement as fact `f001` at 00:57:45 UTC.
6. It created completion intent `i002`, connecting `f001` to the goal because the
   observed win rate exceeded 55%. The server marked the project completed.
7. The one-pass dispatcher exited. `worker-b` was not needed.

All timestamps above are from the exported board and are explicitly UTC.

## Reproduction

From the repository folder:

```sh
python3 -B reproduce.py
```

The original command recorded in fact `f001` was:

```sh
python3 -c 'import random; from pig import hold_at_twenty, hold_at_ten, run_tournament; random.seed(20261028); wins = run_tournament(hold_at_twenty, hold_at_ten, games=10000); assert wins[0] >= 5500'
```

Evidence:

- [Board export](results/cairn-board.json): origin, goal, worker claim, measured fact
  and completion intent, including original local paths and timestamps.
- [Timeline export](results/cairn-timeline.txt): Cairn's readable event sequence;
  its timestamps use the server host's local formatting.
- [Benchmark JSON](results/benchmark.json): exact measurements, seed, original
  simulator SHA-256, reproduction command and limitations.
- [Reproduction output](results/reproduction-output.txt): captured tournament output.

## Conclusion

The experiment met its stated numerical goal: hold-at-20 beat the fixed hold-at-10
opponent in 69.83% of the 10,000 seeded games. Alternating starting positions
gave both strategies the same number of first turns.

The Cairn integration worked: it assigned a task, ran the local simulator through
a Codex worker, stored a fact and marked the goal complete. A bootstrap task can
solve a straightforward objective directly; a separate Reason task or second
worker is not always required.

The strategy was supplied before the run. This is evidence of execution and
measurement, rather than autonomous strategy discovery. One seeded tournament
against a deliberately simple opponent does not establish optimal play or results
against other opponents. The completion claim came from the same worker that
performed the experiment; the later local reproduction strengthens confidence in
the recorded count but does not demonstrate independent multi-agent validation.

## A possible next learning exercise

In a new project, supply the game and baseline without supplying the candidate.
Disable bootstrap and inspect the first Reason task's proposed intents before
continuing. Separate exploration and verification would make sharing the board
and the stopping decision easier to observe. This follow-up has not been run.
