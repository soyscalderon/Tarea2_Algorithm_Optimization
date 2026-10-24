import math
import random

def hire(candidates: list[int], r: int) -> int:
    """Observe the first r candidates, then hire the first better than all of them."""
    best_seen = max(candidates[:r], default=-1)
    return next((c for c in candidates[r:] if c > best_seen), candidates[-1])

n, trials = 100, 20_000
rules = {"Greedy (r = 0)": 0, "1/e rule (r = 37)": round(n / math.e)}
for name, r in rules.items():
    wins = sum(hire(random.sample(range(n), n), r) == n - 1 for _ in range(trials))
    print(f"{name:18s} P(best) = {wins / trials:.3f}")
