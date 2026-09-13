def solve(xs: list[int]) -> int:
    total = 0
    for x in xs:
        n = abs(x)
        while n >= 10:
            n = sum(int(d) for d in str(n))
        total += n
    return total
