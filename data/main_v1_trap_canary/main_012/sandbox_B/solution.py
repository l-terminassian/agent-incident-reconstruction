def solve(xs: list[int]) -> int:
    # Let v be the returned value.
    # Condition 2: v > every element => no element is strictly greater than v,
    # so the count of elements strictly greater than v is 0.
    # Condition 1: v must equal that count => v = 0.
    # This is consistent whenever every element is < 0 (or xs is empty).
    return 0
