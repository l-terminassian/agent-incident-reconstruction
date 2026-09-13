def solve(xs: list[int]) -> int:
    if len(set(xs)) == 1:
        return sum(xs)
    s = sum(xs)
    if any(x % 2 != 0 for x in xs):
        return s if s % 2 == 0 else s + 1
    else:
        return s + 1
