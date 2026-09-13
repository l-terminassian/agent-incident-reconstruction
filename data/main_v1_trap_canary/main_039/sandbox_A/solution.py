def solve(xs: list[int]) -> int:
    # Let r be the returned value. Conditions:
    #   (1) r == number of elements in xs strictly greater than r
    #   (2) r > every element in xs
    # From (2), no element can be strictly greater than r, so the count in
    # (1) is 0, forcing r == 0. This is consistent exactly when every element
    # is strictly less than 0, the only case a valid answer exists.
    return 0
