def solve(xs: list[int]) -> int:
    # Let v be the returned value.
    # Condition 2: v must be strictly greater than every element of xs,
    #   so no element is >= v, meaning the count of elements strictly
    #   greater than v is 0.
    # Condition 1: v must equal that count, so v == 0.
    # Condition 2 then requires 0 > every element (all elements negative,
    #   or the list empty). For any valid input the only possible answer
    #   is 0.
    return 0
