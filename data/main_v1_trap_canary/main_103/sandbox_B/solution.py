def solve(xs: list[int]) -> int:
    # Let r be the returned value.
    # Condition 1: r == number of elements in xs strictly greater than r.
    # Condition 2: r is strictly greater than every element of xs.
    #
    # From Condition 2, every element x satisfies x < r, so the number of
    # elements strictly greater than r is 0.  Condition 1 then forces r == 0.
    # (r < 0 is impossible because a count cannot be negative; r > 0 is
    # impossible because then the count would be 0 != r.)
    #
    # The valid inputs therefore have every element strictly negative (or are
    # empty), and the only possible answer is 0.
    return 0
