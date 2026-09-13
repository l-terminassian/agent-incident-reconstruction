def solve(xs: list[int]) -> int:
    n = len(xs)
    if n < 2:
        return -1
    xs_sorted = sorted(xs, reverse=True)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + xs_sorted[i]
    best = None
    for k in range(2, n + 1):
        if k % 3 == 2:
            s = prefix[k]
            if best is None or s > best:
                best = s
    return best
