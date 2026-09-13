def solve(xs: list[int]) -> int:
    s = sum(xs)
    if len(set(xs)) == 1:
        return s
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    if has_odd:
        if s % 2 != 0:
            s += 1
    elif has_even:
        if s % 2 == 0:
            s += 1
    return s
