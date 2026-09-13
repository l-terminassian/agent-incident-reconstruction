def solve(xs: list[int]) -> int:
    n = len(xs)
    if n == 0:
        return 0
    total = 0
    for i, x in enumerate(xs):
        w = ((i + 1) % n) + 1
        total += x * w
    return total % 97
