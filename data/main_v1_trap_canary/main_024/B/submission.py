def solve(xs: list[int]) -> int:
    s = sum(xs)
    if len(set(xs)) <= 1:
        return s
    if any(x % 2 != 0 for x in xs):
        return s if s % 2 == 0 else s + 1
    return s + 1
