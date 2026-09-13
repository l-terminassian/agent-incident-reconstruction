def solve(xs: list[int]) -> int:
    """Return the length of the longest run of consecutive elements
    that all share the same parity (all even or all odd).
    A single element counts as a run of length 1.
    An empty list has no run, so return 0.
    """
    if not xs:
        return 0
    best = 1
    cur = 1
    prev_parity = xs[0] % 2
    for x in xs[1:]:
        if x % 2 == prev_parity:
            cur += 1
            if cur > best:
                best = cur
        else:
            prev_parity = x % 2
            cur = 1
    return best
