import random
from itertools import combinations
from solution import solve

def brute(xs):
    n = len(xs)
    if n == 0:
        return 0
    best = 1
    for r in range(2, n + 1):
        for comb in combinations(range(n), r):
            seq = [xs[i] for i in comb]
            diffs = [seq[i + 1] - seq[i] for i in range(r - 1)]
            ok = True
            for d in diffs:
                if d == 0:
                    ok = False
                    break
            if not ok:
                continue
            for k in range(1, len(diffs)):
                if (diffs[k] > 0) == (diffs[k - 1] > 0):
                    ok = False
                    break
            if ok:
                best = max(best, r)
    return best

random.seed(1)
for t in range(5000):
    n = random.randint(0, 9)
    xs = [random.randint(-5, 5) for _ in range(n)]
    a = solve(xs)
    b = brute(xs)
    assert a == b, (xs, a, b)
print("all ok")
print(solve([]), solve([1]), solve([1, 1]), solve([1, 7, 4, 9, 2, 5]), solve([1, 17, 5, 10, 13, 15, 10, 5, 16, 8]))
