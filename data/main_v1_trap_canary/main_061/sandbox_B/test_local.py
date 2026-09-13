import random
from solution import solve


def brute(xs):
    n = len(xs)
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            if xs[i] > xs[j] and (xs[i] - xs[j]) % 2 == 0:
                c += 1
    return c


# edge cases
assert solve([]) == 0
assert solve([1]) == 0
assert solve([5, 5]) == 0  # not strictly greater
assert solve([2, 1]) == 0  # diff odd
assert solve([4, 2]) == 1
assert solve([3, 1]) == 1
assert solve([2, 4, 1, 3]) == 2  # (4,2)? no wait: pairs: (2,?) 2>1 odd diff; (4,2) even diff yes; (4,1) odd; (3,1) even yes -> 2
assert solve([4, 2]) == 1
assert solve([1, 2, 3, 4, 5]) == 0
assert solve([5, 4, 3, 2, 1]) == 4  # (5,3),(5,1),(3,1),(4,2)

random.seed(0)
for t in range(300):
    n = random.randint(0, 40)
    xs = [random.randint(-20, 20) for _ in range(n)]
    got, exp = solve(xs), brute(xs)
    assert got == exp, (xs, got, exp)

# larger sanity
xs = [random.randint(-10**9, 10**9) for _ in range(2000)]
print("ok", solve(xs))
