def solve(xs: list[int]) -> int:
    count = 0
    n = len(xs)
    for i in range(n):
        for j in range(i + 1, n):
            if xs[i] > xs[j] and (xs[i] - xs[j]) % 2 == 0:
                count += 1
    return count
