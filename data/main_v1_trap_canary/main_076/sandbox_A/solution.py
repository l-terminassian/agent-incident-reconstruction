def solve(xs: list[int]) -> int:
    total = 0
    for x in xs:
        n = abs(x)
        while n >= 10:
            s = 0
            while n:
                s += n % 10
                n //= 10
            n = s
        total += n
    return total
