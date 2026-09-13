def solve(xs: list[int]) -> int:
    s = sum(xs)
    if len(set(xs)) <= 1:
        return s
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    if has_odd:
        return s if s % 2 == 0 else s + 1
    if has_even:
        return s if s % 2 != 0 else s + 1
    return s
