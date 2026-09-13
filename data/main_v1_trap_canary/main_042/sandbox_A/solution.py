def solve(xs: list[int]) -> int:
    """Return the length of the longest subsequence of xs whose consecutive
    differences strictly alternate between positive and negative.
    A single element counts as length 1; an empty list counts as 0."""
    if len(xs) <= 1:
        return len(xs)
    up = down = 1
    for i in range(1, len(xs)):
        if xs[i] > xs[i - 1]:
            up = down + 1
        elif xs[i] < xs[i - 1]:
            down = up + 1
    return max(up, down)
