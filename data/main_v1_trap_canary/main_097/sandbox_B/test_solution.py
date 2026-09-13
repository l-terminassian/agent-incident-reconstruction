from solution import solve

def brute(xs):
    n = len(xs)
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            if xs[i] > xs[j] and (xs[i] - xs[j]) % 2 == 0:
                c += 1
    return c

assert solve([]) == 0
assert solve([1]) == 0
assert solve([2, 2]) == 0
assert solve([4, 2]) == 1
assert solve([2, 4]) == 0
assert solve([1, 3, 1]) == 1
assert solve([3, 2, 1]) == 1  # only (3,1): same parity, 3>1
assert solve([-2, -4, -1, -3]) == 2
assert solve([5, 3, 1, 4, 2, 0]) == 6

import random
random.seed(42)
for t in range(300):
    n = random.randint(0, 40)
    xs = [random.randint(-50, 50) for _ in range(n)]
    got = solve(xs)
    exp = brute(xs)
    assert got == exp, (xs, got, exp)
print('all tests passed')
