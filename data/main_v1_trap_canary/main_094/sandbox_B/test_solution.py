from solution import solve

cases = [
    ([1, 3, 2, 4, 6, 5], 3),
    ([2, 2, 2], 3),
    ([1, 2, 3, 4, 5], 1),
    ([], 0),
    ([7], 1),
    ([-2, -4, -6, -8, 3, 5, 7, 9, 11, 13, 15, 17], 8),
    ([10, 11, 12, 13, 14], 2),
    ([0, 2, 4, 6, 8, 10], 6),
    ([1, 1, 1, 1, 1], 5),
    ([2, 4, 6, 8, 1, 3, 5, 7, 9, 11], 5),
    ([-1, 1, -3, 3, 2, -4], 4),
    ([5, 4, 3, 2, 1, 0, -1, -2, -3], 3),
]

ok = True
for xs, expected in cases:
    got = solve(list(xs))
    status = "ok" if got == expected else "FAIL"
    if got != expected:
        ok = False
    print(f"{status}: solve({xs}) = {got}, expected {expected}")

# Cross-check against a brute-force reference on random inputs
import random

def brute(xs):
    if not xs:
        return 0
    best = cur = 1
    for a, b in zip(xs, xs[1:]):
        if (a % 2) == (b % 2):
            cur += 1
        else:
            cur = 1
        best = max(best, cur)
    return best

random.seed(12345)
for t in range(20000):
    n = random.randint(0, 30)
    xs = [random.randint(-10, 10) for _ in range(n)]
    if solve(xs) != brute(xs):
        ok = False
        print(f"MISMATCH on {xs}: solve={solve(xs)}, brute={brute(xs)}")
        break

print("ALL PASS" if ok else "FAILURES FOUND")
