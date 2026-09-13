def solve(xs: list[int]) -> int:
    """For each element, take its absolute value and repeatedly replace it by
    the sum of its decimal digits until the result is below 10. Return the
    sum of the collapsed values."""
    def collapse(x: int) -> int:
        x = abs(x)
        while x >= 10:
            s = 0
            while x:
                s += x % 10
                x //= 10
            x = s
        return x
    return sum(collapse(x) for x in xs)
