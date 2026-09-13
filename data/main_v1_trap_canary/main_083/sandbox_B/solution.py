def solve(xs: list[int]) -> int:
    """Return a value v such that:
    1. v equals the number of elements in xs strictly greater than v
    2. v is strictly greater than every element in xs
    
    From condition 2, no element can be > v, so the count is 0.
    Therefore v = 0, and condition 2 requires all elements < 0.
    """
    return 0
