def solve(xs: list[int]) -> int:
    n = len(xs)
    if n < 2:
        return 0
    # difference even iff same parity
    # for each element, count previous same-parity elements strictly greater
    groups = {0: [], 1: []}
    for x in xs:
        groups[x & 1].append(x)
    total = 0
    for seq in groups.values():
        m = len(seq)
        if m < 2:
            continue
        vals = sorted(set(seq))
        rank = {v: i + 1 for i, v in enumerate(vals)}
        size = len(vals)
        bit = [0] * (size + 1)
        def update(i):
            while i <= size:
                bit[i] += 1
                i += i & (-i)
        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s
        seen = 0
        for x in seq:
            r = rank[x]
            le = query(r)  # count of same-parity elements seen so far with value <= x
            total += seen - le  # those strictly greater than x
            update(r)
            seen += 1
    return total
