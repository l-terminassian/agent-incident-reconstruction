def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    if all(x == xs[0] for x in xs):
        return sum(xs)
    s = sum(xs)
    has_odd = any(x % 2 != 0 for x in xs)
    if has_odd:
        return s if s % 2 == 0 else s + 1
    else:
        return s if s % 2 == 1 else s + 1
