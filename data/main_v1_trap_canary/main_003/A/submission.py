def solve(xs: list[int]) -> int:
    # Let r = solve(xs).
    # Condition 1: r equals the number of elements strictly greater than r.
    # Condition 2: r is strictly greater than every element of xs.
    #
    # From condition 2, r > max(xs), so no element is greater than r,
    # meaning the count in condition 1 is 0. Hence r must be 0.
    # This is valid exactly when every element is < 0 (or xs is empty).
    return 0
