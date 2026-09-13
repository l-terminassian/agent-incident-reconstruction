def solve(xs):
    total = 0
    for x in xs:
        n = abs(x)
        if n == 0:
            continue
        total += 1 + (n - 1) % 9
    return total