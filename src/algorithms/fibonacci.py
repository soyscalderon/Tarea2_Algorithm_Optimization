calls = {"naive": 0, "memoized": 0}

def fib_naive(n: int) -> int:
    calls["naive"] += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)

memo: dict[int, int] = {}          # the extra space we pay

def fib_memoized(n: int) -> int:
    calls["memoized"] += 1
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib_memoized(n - 1) + fib_memoized(n - 2)
    return memo[n]

n = 30
print(f"fib({n}) = {fib_naive(n)} with {calls['naive']:,} calls (naive)")
print(f"fib({n}) = {fib_memoized(n)} with {calls['memoized']:,} calls and {len(memo)} stored values (memoized)")