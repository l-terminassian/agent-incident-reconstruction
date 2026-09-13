def solve(xs: list[int]) -> int:
    # k must equal the number of elements strictly greater than k,
    # AND k must be strictly greater than every element of the list.
    #
    # From the second condition, every element x satisfies x < k, so no
    # element is strictly greater than k. Hence count(x > k) == 0, forcing
    # k == 0.
    #
    # k == 0 then satisfies the first condition automatically (0 == 0), and
    # satisfies the second exactly when every element is < 0 (or the list is
    # empty). The problem guarantees a valid answer exists, so returning 0
    # is correct for all valid inputs.
    return 0
