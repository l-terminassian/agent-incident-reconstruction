def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    best = 1
    cur = 1
    for i in range(1, len(xs)):
        if (xs[i] % 2) == (xs[i - 1] % 2):
            cur += 1
        else:
            cur = 1
        if cur > best:
            best = cur
    return best
