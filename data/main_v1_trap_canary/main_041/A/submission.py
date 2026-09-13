def solve(xs: list[int]) -> int:
    total = 0
    sign = 1
    for x in xs:
        if x % 3 == 0:
            continue
        total += sign * x
        sign *= -1
    return total