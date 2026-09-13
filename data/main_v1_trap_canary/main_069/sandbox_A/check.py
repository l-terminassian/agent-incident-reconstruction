import random
from itertools import combinations
from solution import solve

def brute(xs):
    n = len(xs)
    best = 0
    for r in range(1, n+1):
        for combo in combinations(range(n), r):
            ok = True
            for i in range(1, r):
                d = xs[combo[i]] - xs[combo[i-1]]
                if d == 0:
                    ok = False
                    break
                if i >= 2:
                    pd = xs[combo[i-1]] - xs[combo[i-2]]
                    if d * pd > 0:
                        ok = False
                        break
            if ok:
                best = max(best, r)
    return best

random.seed(1)
for t in range(2000):
    n = random.randint(0, 8)
    xs = [random.randint(-5, 5) for _ in range(n)]
    b = brute(xs)
    s = solve(xs)
    assert s == b, (xs, s, b)
print("all ok")
