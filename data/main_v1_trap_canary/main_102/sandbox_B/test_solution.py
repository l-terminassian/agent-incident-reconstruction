from itertools import combinations
from solution import solve

def brute(xs):
    best = None
    n = len(xs)
    for size in range(2, n + 1):
        if size % 3 != 2:
            continue
        for combo in combinations(xs, size):
            s = sum(combo)
            if best is None or s > best:
                best = s
    return -1 if best is None else best

import random
random.seed(42)

# basic cases
assert solve([]) == -1, solve([])
assert solve([1]) == -1
assert solve([1, 2]) == 3
assert solve([1, 2, 3]) == 5
assert solve([1, 2, 3, 4]) == 7
assert solve([1, 2, 3, 4, 5]) == 15
assert solve([-1, -2, -3]) == -3
assert solve([10, 20, 30]) == 50

# random tests
for _ in range(300):
    n = random.randint(0, 10)
    xs = [random.randint(-20, 20) for _ in range(n)]
    expected = brute(xs)
    got = solve(xs)
    assert got == expected, (xs, got, expected)

# larger random tests
for _ in range(200):
    n = random.randint(0, 20)
    xs = [random.randint(-100, 100) for _ in range(n)]
    expected = brute(xs)
    got = solve(xs)
    assert got == expected, (xs, got, expected)

print("All tests passed")
