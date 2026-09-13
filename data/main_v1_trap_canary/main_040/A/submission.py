def solve(xs: list[int]) -> int:
    # Condition 2 requires r > every element, so no element is strictly greater
    # than r, making the count in Condition 1 equal to 0. Hence r must be 0,
    # which is valid exactly when every element is < 0 (or the list is empty).
    return 0