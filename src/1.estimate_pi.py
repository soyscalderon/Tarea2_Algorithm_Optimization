import argparse
import time
import multiprocessing as mp
import random
import math

def estimate_pi(seed: int, samples: int = 1_000_000) -> float:
    """Monte Carlo: fraction of random points that fall inside the unit quarter circle."""
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monte Carlo estimation of pi.")
    parser.add_argument("--graph", action="store_true",
                        help="Also generate the matplotlib figures.")
    args = parser.parse_args()

    seeds = list(range(8))  # 8 independent runs, one seed each

    # 1. Sequential Looping
    t0 = time.perf_counter()
    seq_results = [estimate_pi(s) for s in seeds]
    t_seq = time.perf_counter() - t0

    # 2. Different number of processes
    parallel_processes_num = [1,2,4,8,mp.cpu_count()]
    parallel_times = []
    parallel_results =[]
    for n in parallel_processes_num:
        t0 = time.perf_counter()
        with mp.Pool(processes=n) as pool:
            parallel_results.append(pool.map(estimate_pi, seeds))
        parallel_times.append(time.perf_counter() - t0)


    print("Pi Estimation (Sequential, Parallel and different Sample Sizes)\n")
    # Print sequential and parallel results
    print(f"Sequential wall-clock: {t_seq:.3f} s")
    print(f"pi estimate (mean of {len(seeds)} runs): {sum(seq_results) / len(seq_results):.5f}\n")
    for n in range(len(parallel_processes_num)):
        print(f"Parallel (# processes={parallel_processes_num[n]}) wall-clock:   {parallel_times[n]:.3f} s (Speedup vs Sequential: {t_seq/parallel_times[n]:.2f}x)")
        print(f"pi estimate (mean of {len(seeds)} runs): {sum(parallel_results[n]) / len(parallel_results[n]):.5f}\n")

    # 3. Different sample sizes
    random.seed(1)
    print("Estimation with different sample sizes")
    for samples in [10**2, 10**3, 10**4, 10**5, 10**6]:
        estimate = estimate_pi(1,samples)
        print(f"# Samples = {samples:>9,}   pi ~ {estimate:.5f}   error = {abs(estimate-math.pi):.5f}   1/sqrt(# Samples) = {1 / math.sqrt(samples):.5f}")

# Graficas
if __name__ == "__main__" and args.graph:
    import matplotlib.pyplot as plt
    from pathlib import Path

    figure_directory = Path(__file__).resolve().parents[1] / "graphs"
    figure_directory.mkdir(parents=True, exist_ok=True)

    speedup_values = [t_seq / parallel_time for parallel_time in parallel_times]
    ideal_speedup_values = list(parallel_processes_num)       # ideal: speedup = #processes

    speedup_figure, speedup_axis = plt.subplots(figsize=(7, 5))
    speedup_axis.plot(parallel_processes_num, speedup_values, "o-", linewidth=2,
                      markersize=8, label="Observed speedup")
    speedup_axis.plot(parallel_processes_num, ideal_speedup_values, "k--",
                      label="Ideal speedup (n)")
    speedup_axis.set_xlabel("Number of processes")
    speedup_axis.set_ylabel("Speedup (t sequential / t parallel)")
    speedup_axis.set_title("Parallel speedup of estimate_pi (8 independent runs)")
    speedup_axis.set_xticks(parallel_processes_num)
    speedup_axis.grid(alpha=0.3)
    speedup_axis.legend()
    speedup_figure.tight_layout()

    speedup_path = figure_directory / "1.parallel_speedup.png"
    speedup_figure.savefig(speedup_path, dpi=150)
    print(f"\nFigure saved to {speedup_path}")
    