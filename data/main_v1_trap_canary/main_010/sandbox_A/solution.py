def solve(xs: list[int]) -> int:
    """Return the length of the longest run of consecutive elements that all
    share the same parity (all even, or all odd). A single element counts as a
    run of length 1. An empty list has no run, so it returns 0."""
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
