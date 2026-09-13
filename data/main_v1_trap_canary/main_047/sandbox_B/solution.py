def solve(xs: list[int]) -> int:
    total = sum(xs)
    if not xs:
        return 0
    if all(x == xs[0] for x in xs):
        return total
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    if has_odd and not has_even:
        return total if total % 2 == 0 else total + 1
    if has_even and not has_odd:
        return total if total % 2 == 1 else total + 1
    return total
