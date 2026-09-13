def solve(xs: list[int]) -> int:
    """For each element, take its absolute value and repeatedly replace it by
    the sum of its decimal digits until the result is below 10.
    Return the sum of the collapsed values."""
    total = 0
    for x in xs:
        n = abs(x)
        while n >= 10:
            s = 0
            while n > 0:
                s += n % 10
                n //= 10
            n = s
        total += n
    return total
