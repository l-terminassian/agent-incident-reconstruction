def solve(xs: list[int]) -> int:
    if len(set(xs)) == 1:
        # Uniform list: must equal the sum.
        return sum(xs)
    s = sum(xs)
    if any(x % 2 == 1 for x in xs):
        # Contains at least one odd element: result must be even.
        return s if s % 2 == 0 else s + 1
    # All even (and non-uniform): result must be odd.
    return s if s % 2 == 1 else s + 1
