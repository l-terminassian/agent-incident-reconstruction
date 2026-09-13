def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    if len(set(xs)) == 1:
        return sum(xs)
    s = sum(xs)
    has_odd = any(x % 2 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    if has_odd and not has_even:
        return s if s % 2 == 0 else s + 1
    if has_even and not has_odd:
        return s if s % 2 == 1 else s + 1
    return s if s % 2 == 0 else s + 1
