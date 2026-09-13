def solve(xs: list[int]) -> int:
    # The returned value r must satisfy:
    # 1) r == count of elements in xs that are strictly greater than r
    # 2) r is strictly greater than every element of xs
    #
    # From (2), every element x in xs satisfies x < r.
    # Then the number of elements strictly greater than r is 0.
    # So (1) forces r == 0.
    # And (2) then requires every element to be < 0 (vacuously true if xs is empty).
    # For all valid inputs the unique answer is 0.
    return 0
