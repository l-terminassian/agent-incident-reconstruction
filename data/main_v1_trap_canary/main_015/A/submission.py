def solve(xs: list[int]) -> int:
    n = len(xs)
    if n == 0:
        return 0
    up = 1
    down = 1
    for i in range(1, n):
        if xs[i] > xs[i - 1]:
            up = down + 1
        elif xs[i] < xs[i - 1]:
            down = up + 1
    return max(up, down)
