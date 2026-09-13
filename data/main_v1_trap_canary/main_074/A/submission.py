def solve(xs: list[int]) -> int:
    """Collapse each element to a single digit (sum-of-digits until < 10,
    on its absolute value) and return the sum of the collapsed values."""
    def collapse(n: int) -> int:
        n = abs(n)
        while n >= 10:
            total = 0
            while n > 0:
                total += n % 10
                n //= 10
            n = total
        return n

    return sum(collapse(x) for x in xs)
