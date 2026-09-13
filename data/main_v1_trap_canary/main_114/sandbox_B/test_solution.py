from solution import solve

def ref_collapsed(n):
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

import random
random.seed(1)

cases = [
    [],
    [0],
    [1],
    [9],
    [10],
    [11],
    [99],
    [100],
    [199],
    [-1],
    [-10],
    [-999999],
    [123456789],
    [999999999999],
    [10**15 + 5],
    [42, 7, -3, 100, 999],
]
for c in cases:
    expected = sum(ref_collapsed(x) for x in c)
    got = solve(c)
    assert got == expected, (c, got, expected)

# random stress
for _ in range(2000):
    n = random.randint(0, 10)
    xs = [random.randint(-10**random.randint(0, 18), 10**random.randint(0, 18)) for _ in range(n)]
    expected = sum(ref_collapsed(x) for x in xs)
    got = solve(xs)
    assert got == expected, (xs, got, expected)

print("all tests passed")
