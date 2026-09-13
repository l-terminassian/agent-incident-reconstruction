def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    if len(set(xs)) == 1:
        return sum(xs)
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    s = sum(xs)
    if has_odd:
        # must be even
        return s if s % 2 == 0 else s + 1
    elif has_even:
        # must be odd
        return s if s % 2 != 0 else s + 1
    else:
        return s
