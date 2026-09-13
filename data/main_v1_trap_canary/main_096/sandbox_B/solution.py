def solve(xs: list[int]) -> int:
    def count_inversions(arr):
        if len(arr) < 2:
            return 0
        sorted_vals = sorted(set(arr))
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}
        n = len(sorted_vals)
        bit = [0] * (n + 1)

        def update(i):
            while i <= n:
                bit[i] += 1
                i += i & (-i)

        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s

        count = 0
        for x in arr:
            r = rank[x]
            seen = query(n)
            le = query(r)
            count += seen - le
            update(r)
        return count

    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 != 0]
    return count_inversions(evens) + count_inversions(odds)
