def solve(xs: list[int]) -> int:
    if len(xs) == 0:
        return 0
    if all(x == xs[0] for x in xs):
        return sum(xs)
    if any(x % 2 != 0 for x in xs):
        return 0
    return 1