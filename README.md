# Maze Generation Analysis

A Python project I built between June and August 2024 that generates and solves mazes, visualizes the process through a Pygame UI, and measures how random the generation actually is.

## What it does

- Generates a maze using a recursive backtracking algorithm.
- Solves the generated maze and optionally highlights backtracking steps.
- Lets me watch generation and solving happen in real time, or skip the animation.
- Runs an analysis pass that converts the finished maze into a numerical matrix, builds a probability distribution over the 14 possible cell shapes, and computes Shannon's entropy.
- Tracks the count and percentage of each direction chosen during generation (up, down, left, right) and renders it as a bar chart with matplotlib.

## Project layout

```
src/
  main.py            entry point
  app.py             screen, grid dimensions, cell size
  cell.py            a single maze cell and its walls
  maze.py            generation and solving logic
  game.py            game loop, UI orchestration, graph rendering
  maze_controls.py   buttons, sliders, checkboxes, text
  analysis.py        matrix conversion, probability distribution, entropy
  random_sample.py   my modified Fisher-Yates sampler
  constants.py       colors
tests/
  test_entropy.py    randomness assessment on sample number blocks
data/
  data.txt           persisted direction counts across runs
```

## Why I refactored random.sample

The generator picks the next direction by sampling from a 4-element compass list. Originally I called `random.sample` directly. I wanted to know whether I could get a "more random" result for this specific use case, so I rewrote it as a Fisher-Yates shuffle backed by `secrets.randbelow` instead of the Mersenne Twister that `random` uses by default. The implementation lives in [random_sample.py](src/random_sample.py) and gets called from [maze.py:47](src/maze.py).

I want to be upfront about what this means. I am not claiming to have mathematically beaten `random.sample`. The CPython implementation is well studied and on a general sample space my version is not better in any formal sense. The point is narrower than that. The maze grid is rectangular, the compass is always exactly four directions, and the recursive backtracker has structural biases that compound with whatever the sampler does. Under those constraints, swapping in a Fisher-Yates shuffle that draws from a cryptographic source produced direction distributions that were measurably closer to uniform in my testing, and the resulting mazes looked less patterned. So "more random" here is a statement about this maze, not about sampling in general.

## How I measured randomness

Two things get measured:

1. Direction selection during generation. Every time the generator picks a direction, [analysis.py](src/analysis.py) increments a counter. The data persists to `data/data.txt` and a bar chart shows the count per direction. With a perfectly uniform sampler the four bars would be equal.
2. Maze structure after generation. Each cell has one of 14 possible wall configurations (four walls, with the all-walls and no-walls cases excluded by the algorithm). I convert the maze to a matrix of these 14 values, compute the probability distribution, and feed it into Shannon's entropy. The theoretical maximum for 14 outcomes is `log2(14) ≈ 3.807`, so the closer the computed entropy gets to that, the more uniformly the cell shapes are spread across the maze.

I also have a small randomness-assessment harness in [test_entropy.py](tests/test_entropy.py) that runs the same entropy calculation against fixed number blocks. One thing it makes clear is that this metric works on combinations rather than permutations, so it can flag a skewed distribution but it cannot catch a sequence that is uniform overall while being predictable in order.

## Running it

```
python src/main.py
```

The window opens with controls for cell size, whether to animate generation, whether to highlight backtracking, whether to animate the solver, and a small time-delay toggle. After generation, clicking two cells solves between them. The "Analyze" view shows the entropy, the probability distribution, and the direction-count graph.
