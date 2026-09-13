def solve(xs: list[int]) -> int:
    n = len(xs)
    if n == 0:
        return 0
    total = 0
    for i, x in enumerate(xs):
        weight = ((i + 1) % n) + 1
        total += x * weight
    return total % 97
