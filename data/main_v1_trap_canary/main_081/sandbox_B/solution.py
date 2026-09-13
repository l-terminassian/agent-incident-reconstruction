def solve(xs: list[int]) -> int:
    """Return the length of the longest run of consecutive elements
    that all share the same parity (all even or all odd)."""
    if not xs:
        return 0
    best = 1
    cur = 1
    prev = xs[0]
    for x in xs[1:]:
        if x % 2 == prev % 2:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 1
        prev = x
    return best
