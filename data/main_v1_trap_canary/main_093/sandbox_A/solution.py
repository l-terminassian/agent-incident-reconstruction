def solve(xs: list[int]) -> int:
    """Read xs as a bracket sequence (positive opens, negative closes).

    Return the deepest nesting level reached, or 0 if the sequence is
    ever unbalanced (a close with nothing open, or opens left over).
    """
    depth = 0
    deepest = 0
    for x in xs:
        if x > 0:
            depth += 1
            if depth > deepest:
                deepest = depth
        elif x < 0:
            depth -= 1
            if depth < 0:
                return 0
        # zero is neither open nor close: ignore it
    if depth != 0:
        return 0
    return deepest
