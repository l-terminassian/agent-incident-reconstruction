def solve(xs: list[int]) -> int:
    # Let r be the returned value.
    # Condition A: r == number of elements in xs strictly greater than r.
    # Condition B: r is strictly greater than every element in xs.
    #
    # From B, no element of xs can be strictly greater than r,
    # so the count in A is 0, forcing r == 0.
    # 0 satisfies B iff every element of xs is < 0 (or xs is empty).
    #
    # Therefore the unique valid answer is 0, valid exactly when
    # all elements are negative (or the list is empty).
    return 0
