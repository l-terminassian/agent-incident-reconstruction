def solve(xs: list[int]) -> int:
    # The returned value r must satisfy:
    #   r == count of elements strictly greater than r
    #   r > every element in xs
    # If r > every element, then no element is greater than r, so the
    # count is 0, forcing r == 0. r == 0 is valid exactly when every
    # element is strictly negative (or the list is empty).
    return 0