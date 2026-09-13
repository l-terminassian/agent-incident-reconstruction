def solve(xs: list[int]) -> int:
    """Read xs as a bracket sequence (positive opens, negative closes).

    Return the deepest nesting level reached. Return 0 if the sequence is
    unbalanced (a close with nothing open, or opens left over at the end).
    """
    depth = 0
    max_depth = 0
    for x in xs:
        if x > 0:
            depth += 1
            if depth > max_depth:
                max_depth = depth
        elif x < 0:
            depth -= 1
            if depth < 0:
                return 0
        # zero is neither an open nor a close: no effect on balance/depth
    if depth != 0:
        return 0
    return max_depth
