def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    s = sum(xs)
    # Condition 3: if the list is uniform, the result must equal the sum.
    if len(set(xs)) == 1:
        return s
    has_odd = any(x % 2 != 0 for x in xs)
    has_even = any(x % 2 == 0 for x in xs)
    # Condition 1: even whenever at least one odd element.
    if has_odd:
        return s if s % 2 == 0 else s + 1
    # Condition 2: odd whenever at least one even element.
    if has_even:
        return s if s % 2 != 0 else s + 1
    return s
