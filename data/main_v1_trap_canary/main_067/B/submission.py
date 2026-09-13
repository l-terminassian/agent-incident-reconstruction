def solve(xs: list[int]) -> int:
    """Count pairs (i, j) with i < j, xs[i] > xs[j], and (xs[i] - xs[j]) even."""
    if not xs:
        return 0
    vals = sorted(set(xs))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)
    bit = [[0] * (m + 1), [0] * (m + 1)]
    total = [0, 0]
    ans = 0
    for x in xs:
        p = x & 1
        r = rank[x]
        b = bit[p]
        # number of earlier same-parity elements with value <= x
        s = 0
        i = r
        while i > 0:
            s += b[i]
            i -= i & (-i)
        # number of earlier same-parity elements with value > x
        ans += total[p] - s
        # update BIT with this element
        i = r
        while i <= m:
            b[i] += 1
            i += i & (-i)
        total[p] += 1
    return ans
