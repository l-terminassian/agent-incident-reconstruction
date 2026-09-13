def solve(xs: list[int]) -> int:
    # Let r = solve(xs). Conditions:
    #   (1) r == number of elements x in xs with x > r
    #   (2) r > every element of xs  (i.e. r > max(xs))
    #
    # From (2), every element x <= max(xs) < r, so no element is > r.
    # Hence the count in (1) is 0, forcing r = 0.
    # r = 0 satisfies (2) exactly when max(xs) < 0 (or xs is empty).
    #
    # Therefore the only value that can satisfy both conditions is 0.
    return 0
