def solve(xs: list[int]) -> int:
    if len(xs) == 0:
        return 0
    if all(x == xs[0] for x in xs):
        return xs[0]
    return sum(x * (i + 1) for i, x in enumerate(xs))
