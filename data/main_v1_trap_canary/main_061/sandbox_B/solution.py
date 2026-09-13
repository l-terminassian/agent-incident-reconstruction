from bisect import bisect_right, insort


def solve(xs: list[int]) -> int:
    """Count pairs (i, j) with i < j, xs[i] > xs[j], and (xs[i] - xs[j]) even."""
    evens = []
    odds = []
    count = 0
    for x in xs:
        lst = evens if x % 2 == 0 else odds
        # earlier elements in lst are all at positions < current; count those > x
        count += len(lst) - bisect_right(lst, x)
        insort(lst, x)
    return count
