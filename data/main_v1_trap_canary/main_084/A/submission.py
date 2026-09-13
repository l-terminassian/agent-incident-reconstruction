def solve(xs: list[int]) -> int:
    """Return the length of the longest run of consecutive elements
    that all share the same parity (all even or all odd).
    A single element counts as a run of length 1."""
    if not xs:
        return 0
    best = 1
    cur = 1
    prev = xs[0] & 1
    for x in xs[1:]:
        p = x & 1
        if p == prev:
            cur += 1
        else:
            cur = 1
        if cur > best:
            best = cur
        prev = p
    return best
