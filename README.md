# Tarea 2 — Análisis y Optimización de Algoritmos

Experiments for the second assignment of the course. Each exercise implements a
classic algorithm or heuristic and **compares different approaches to the same
problem in terms of time and quality**, backing the analysis with generated
graphs.

## Contents

```
├── src/        # one script per exercise (1-5)
├── graphs/     # figures generated with --graph
├── docs/       # instructions, analysis answers, presentation, demo video
├── exec.sh     # runs every script
└── graph.sh    # runs every script with --graph
```

| Script | Experiment | Graph |
| ------ | ---------- | ----- |
| `src/1.estimate_pi.py` | Parallel speedup of `estimate_pi` with 1–8+ processes vs. the ideal line | `1.parallel_speedup.png` |
| `src/2.knapsack.py` | Greedy knapsack: least weight first vs. value/weight ratio | `2.knapsack_greedy.png` |
| `src/3.TSP.py` | 2-opt local search for the TSP from a random vs. nearest-neighbour start | `3.tsp_2opt_initialization.png` |
| `src/4.simulated_annealing.py` | Simulated annealing with linear and exponential cooling schedules | `4.sa_convergence.png`, `4.sa_time_vs_quality.png` |
| `src/5.MST.py` | MST approximation ratio over 100 instances and comparison of TSP methods | `5.mst_approximation_ratio.png`, `5.mst_method_comparison.png` |

## Running

```bash
./exec.sh      # run all the experiments (console output)
./graph.sh     # generate the figures into graphs/
```

Each script can also be run on its own; the `--graph` flag generates its
figures:

```bash
python3 src/1.estimate_pi.py --graph
```

The assignment statement, the answers to the analysis questions and the
presentation materials live in [`docs/`](docs/).
