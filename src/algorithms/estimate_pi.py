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
    seeds = list(range(8))  # 8 independent runs, one seed each

    # 1. Sequential Looping
    t0 = time.perf_counter()
    seq_results = [estimate_pi(s) for s in seeds]
    t_seq = time.perf_counter() - t0

    # 2. Parallel Pool Execution
    t0 = time.perf_counter()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        par_results = pool.map(estimate_pi, seeds)
    t_par = time.perf_counter() - t0

    print(f"Sequential wall-clock: {t_seq:.3f} s")
    print(f"pi estimate (mean of {len(seeds)} runs): {sum(seq_results) / len(seq_results):.5f}\n")
    print(f"Parallel wall-clock:   {t_par:.3f} s (Speedup: {t_seq/t_par:.2f}x)")
    print(f"pi estimate (mean of {len(seeds)} runs): {sum(par_results) / len(par_results):.5f}\n")

    # 3. Different sample sizes
    random.seed(1)
    for samples in [10**2, 10**3, 10**4, 10**5, 10**6]:
        estimate = estimate_pi(1,samples)
        print(f"N = {samples:>9,}   pi ~ {estimate:.5f}   error = {abs(estimate - math.pi):.5f}   1/sqrt(N) = {1 / math.sqrt(samples):.5f}")