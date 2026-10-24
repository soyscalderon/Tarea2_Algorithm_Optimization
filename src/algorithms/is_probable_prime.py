import random

def is_probable_prime(n: int, k: int = 20) -> bool:
    """Miller-Rabin: 'False' is always right; 'True' is wrong with probability <= 4^-k."""
    if n < 4:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for _ in range(k):
        x = pow(random.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False          # found a witness: n is certainly composite
    return True                   # probably prime

if __name__ == "__main__":
    for n in [561, 7919, 2**61 - 1, 2**61 + 1]:
        print(f"{n:>22,}: {'probably prime' if is_probable_prime(n) else 'composite'}")