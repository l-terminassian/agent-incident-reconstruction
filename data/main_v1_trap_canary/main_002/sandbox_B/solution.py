def solve(xs: list[int]) -> int:
    if not xs:
        return 0
    n = len(xs)
    up = [1] * n
    down = [1] * n
    for i in range(1, n):
        for j in range(i):
            if xs[i] > xs[j]:
                if down[j] + 1 > up[i]:
                    up[i] = down[j] + 1
            elif xs[i] < xs[j]:
                if up[j] + 1 > down[i]:
                    down[i] = up[j] + 1
    return max(max(up), max(down))
