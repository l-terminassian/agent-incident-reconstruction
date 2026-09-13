def solve(xs: list[int]) -> int:
    if len(xs) <= 1:
        return len(xs)
    up = 1
    down = 1
    for i in range(1, len(xs)):
        if xs[i] > xs[i - 1]:
            up = down + 1
        elif xs[i] < xs[i - 1]:
            down = up + 1
    return max(up, down)