def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    if all(x == xs[0] for x in xs):
        return sum(xs)
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    if has_odd:
        return 2
    if has_even:
        return 1
    return 0
