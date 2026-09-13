def solve(xs: list[int]) -> int:
    """Count ordered pairs (i, j) with i < j where xs[i] > xs[j]
    and their difference is even (i.e., same parity)."""
    n = len(xs)
    if n < 2:
        return 0

    # Separate by parity; within each parity group, count inversions
    # (pairs i<j with xs[i] > xs[j]).
    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 != 0]

    def count_inversions(arr):
        if len(arr) < 2:
            return 0
        # Coordinate compression
        sorted_unique = sorted(set(arr))
        rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
        size = len(sorted_unique)
        tree = [0] * (size + 1)

        def update(i):
            while i <= size:
                tree[i] += 1
                i += i & (-i)

        def query(i):
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        count = 0
        for x in arr:
            r = rank[x]
            # number of previously seen elements strictly greater than x
            count += (query(size) - query(r))
            update(r)
        return count

    return count_inversions(evens) + count_inversions(odds)
