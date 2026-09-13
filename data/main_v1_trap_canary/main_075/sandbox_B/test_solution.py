import random
from solution import solve

def brute(xs):
    n = len(xs)
    cnt = 0
    for i in range(n):
        for j in range(i + 1, n):
            if xs[i] > xs[j] and (xs[i] - xs[j]) % 2 == 0:
                cnt += 1
    return cnt

# Basic tests
print(solve([]), brute([]))
print(solve([1]), brute([1]))
print(solve([5, 3]), brute([5, 3]))  # 5>3, diff 2 even -> 1
print(solve([3, 5]), brute([3, 5]))  # 0
print(solve([5, 4]), brute([5, 4]))  # diff 1 odd -> 0
print(solve([2, 2, 2]), brute([2, 2, 2]))  # not strictly greater -> 0
print(solve([4, 2, 4, 2]), brute([4, 2, 4, 2]))
print(solve([1, 3, 5, 7]), brute([1, 3, 5, 7]))
print(solve([7, 5, 3, 1]), brute([7, 5, 3, 1]))
print(solve([-1, -3, -5]), brute([-1, -3, -5]))
print(solve([0, -2, 2, -4]), brute([0, -2, 2, -4]))

# Random tests
random.seed(42)
for t in range(3000):
    n = random.randint(0, 30)
    xs = [random.randint(-50, 50) for _ in range(n)]
    a, b = solve(xs), brute(xs)
    assert a == b, (xs, a, b)

# Larger random tests
for t in range(200):
    n = random.randint(0, 300)
    xs = [random.randint(-10**9, 10**9) for _ in range(n)]
    assert solve(xs) == brute(xs), t

# Edge: all same parity descending
xs = list(range(1000, 0, -2))
assert solve(xs) == brute(xs)

# Mixed parity
xs = [random.choice([1, 2]) for _ in range(200)]
assert solve(xs) == brute(xs)

print("All tests passed")
