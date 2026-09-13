def solve(xs: list[int]) -> int:
    def collapse(n: int) -> int:
        n = abs(n)
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n
    return sum(collapse(x) for x in xs)
