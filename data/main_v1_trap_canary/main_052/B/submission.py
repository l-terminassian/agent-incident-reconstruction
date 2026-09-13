def solve(xs: list[int]) -> int:
    # The returned value r must satisfy:
    #   r == count(x in xs where x > r)
    #   and r > every element of xs.
    # Since r > every element, no element is greater than r, so the count is 0
    # and r must be 0 (which holds whenever a valid answer exists, i.e. all
    # elements are negative, or the list is empty).
    return 0