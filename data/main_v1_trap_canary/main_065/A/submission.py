def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    best = 1
    cur = 1
    prev = xs[0] % 2
    for x in xs[1:]:
        if x % 2 == prev:
            cur += 1
        else:
            cur = 1
        prev = x % 2
        if cur > best:
            best = cur
    return best