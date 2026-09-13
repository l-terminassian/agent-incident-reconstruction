import random
from solution import solve

def brute(xs):
    n = len(xs)
    if n == 0:
        return 0
    best = 1
    for mask in range(1, 1 << n):
        sub = [xs[i] for i in range(n) if mask & (1 << i)]
        ok = True
        prev = 0
        for i in range(1, len(sub)):
            d = sub[i] - sub[i-1]
            if d == 0:
                ok = False
                break
            if prev == 0:
                prev = d
            else:
                if (d > 0) == (prev > 0):
                    ok = False
                    break
                prev = d
        if ok:
            best = max(best, len(sub))
    return best

random.seed(1)
for trial in range(500):
    n = random.randint(0, 10)
    xs = [random.randint(-3, 3) for _ in range(n)]
    got = solve(xs)
    exp = brute(xs)
    if got != exp:
        print("MISMATCH", xs, "got", got, "exp", exp)
        break
else:
    print("ALL OK")
