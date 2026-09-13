def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    n = len(xs)
    if n == 1:
        return 1
    up = 1
    down = 1
    for i in range(1, n):
        if xs[i] > xs[i-1]:
            up = down + 1
        elif xs[i] < xs[i-1]:
            down = up + 1
    return max(up, down)
