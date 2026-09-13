def solve(xs: list[int]) -> int:
    # The returned value r must satisfy:
    #   (A) r == number of elements strictly greater than r
    #   (B) r is strictly greater than every element of xs
    # Condition (B) implies there are no elements greater than r, so the
    # count in (A) is 0, forcing r == 0.
    return 0