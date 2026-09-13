def solve(xs: list[int]) -> int:
    """Read xs as a bracket sequence (positive opens, negative closes).

    Return the deepest nesting level reached, or 0 if the sequence is
    unbalanced (a close with nothing open, or opens left over at the end).
    """
    level = 0
    deepest = 0
    for x in xs:
        if x > 0:
            level += 1
            if level > deepest:
                deepest = level
        elif x < 0:
            level -= 1
            if level < 0:
                return 0
        # zero (or any non-bracket value) is a no-op
    if level != 0:
        return 0
    return deepest
