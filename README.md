# Tarea 2 — Análisis y Optimización de Algoritmos

Collection of experiments for the second assignment of the course. The goal is to
implement several classic algorithms and heuristics, run controlled experiments on
them, and **compare different approaches to the same problem in terms of time and
space complexity** using graphs.

The emphasis is not on any single algorithm, but on the *comparison*: how a
different pivot choice, a different greedy criterion, a different starting
solution, a different cooling schedule, or a different memory trade-off changes
the observed cost. Results are produced by running the code and are collected as
figures, so the content of this repository grows as new experiments are added.

## What you will find

- **Implementations** of the algorithms and heuristics used across the exercises,
  under [`src/algorithms/`](src/algorithms/).
- **Experiments** that measure runtime, number of operations, memory usage,
  solution quality, or speedup, depending on the experiment.
- **Graphs** generated from those measurements, stored in
  [`resources/graph_pngs/`](resources/graph_pngs), comparing the different
  approaches of each experiment side by side.
- The assignment statement in [`instructions.md`](instructions.md) and a short
  outline of the topics in [`presentation_exercises.md`](presentation_exercises.md).

## Comparisons at a glance

Each experiment contrasts at least two approaches to the same problem:

| Dimension  | What is measured                                        |
| ---------- | -------------------------------------------------------- |
| Time       | Runtime, speedup vs. number of processes, number of operations, convergence curves |
| Space      | Memory usage and number of subproblems actually computed |
| Quality    | Solution cost, approximation ratio, number of improvements to reach a local optimum |

## Running the experiments

```bash
./exec.sh
```

or run any experiment module directly with `python3`. Generated figures are
written to `resources/graph_pngs/`.

> Note: this README describes the project in general terms; sections and figures
> are updated as the experiments are extended.
