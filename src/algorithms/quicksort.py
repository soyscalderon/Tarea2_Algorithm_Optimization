import math
import random
import sys

sys.setrecursionlimit(10_000)

def quicksort(a: list[int], pick_pivot, counter: list[int]) -> list[int]:
    if len(a) <= 1:
        return a
    p = pick_pivot(a)
    counter[0] += len(a) - 1                         # comparisons against the pivot
    left = [x for x in a if x < p]
    right = [x for x in a if x > p]
    return quicksort(left, pick_pivot, counter) + [p] + quicksort(right, pick_pivot, counter)

n = 2_000
data = list(range(n))                                # already sorted: worst case for a fixed pivot
for name, pick in {"First element": lambda a: a[0], "Random pivot": random.choice}.items():
    counter = [0]
    assert quicksort(data, pick, counter) == data    # Las Vegas: the answer is always correct
    print(f"{name:14s} comparisons = {counter[0]:>9,}")
print(f"{'n log2 n':14s}             = {round(n * math.log2(n)):>9,}")