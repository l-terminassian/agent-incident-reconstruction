def solve(xs: list[int]) -> int:
    # The returned value r must satisfy:
    # 1. r == count of elements in xs strictly greater than r
    # 2. r > every element in xs (i.e., r > max(xs))
    #
    # From condition 2, r > max(xs) means no element is strictly greater than r,
    # so the count in condition 1 is 0. Thus r must be 0.
    # This is valid when all elements are negative (or xs is empty).
    return 0
