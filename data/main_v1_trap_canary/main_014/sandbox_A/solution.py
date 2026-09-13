def solve(xs: list[int]) -> int:
    n = len(xs)
    if n == 0:
        return 0
    up = [1] * n
    down = [1] * n
    for i in range(n):
        for j in range(i):
            if xs[i] > xs[j]:
                up[i] = max(up[i], down[j] + 1)
            elif xs[i] < xs[j]:
                down[i] = max(down[i], up[j] + 1)
    return max(max(up), max(down))
