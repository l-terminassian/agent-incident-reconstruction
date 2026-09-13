def solve(xs):
    s = sum(xs)
    if not xs:
        return 0
    if len(set(xs)) == 1:
        return s
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    if has_odd and not has_even:
        return s if s % 2 == 0 else s + 1
    if has_even and not has_odd:
        return s + 1
    return s