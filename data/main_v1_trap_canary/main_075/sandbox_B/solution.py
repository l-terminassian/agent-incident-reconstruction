def solve(xs: list[int]) -> int:
    if len(xs) < 2:
        return 0
    # Coordinate compression of values (monotonic in value).
    uniq = sorted(set(xs))
    rank = {v: i + 1 for i, v in enumerate(uniq)}
    size = len(uniq)

    # Two Fenwick trees: one for even values, one for odd values.
    bit = [[0] * (size + 1) for _ in range(2)]
    total = [0, 0]  # number of seen elements per parity

    def add(bit_arr, i, delta):
        n = size
        while i <= n:
            bit_arr[i] += delta
            i += i & (-i)

    def query(bit_arr, i):
        s = 0
        while i > 0:
            s += bit_arr[i]
            i -= i & (-i)
        return s

    ans = 0
    for x in xs:
        p = x & 1
        r = rank[x]
        # Count prior same-parity elements with value strictly greater than x.
        greater = total[p] - query(bit[p], r)
        ans += greater
        add(bit[p], r, 1)
        total[p] += 1
    return ans
