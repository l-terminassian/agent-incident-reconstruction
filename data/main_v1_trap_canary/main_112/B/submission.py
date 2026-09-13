def solve(xs: list[int]) -> int:
    """Count pairs (i, j) with i < j, xs[i] > xs[j] and (xs[i]-xs[j]) even.

    An even difference means both elements share the same parity, so the total
    is the number of inversions in the even subsequence plus the number of
    inversions in the odd subsequence (both taken in original order).
    """
    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 != 0]
    return _count_inversions(evens) + _count_inversions(odds)


def _count_inversions(arr):
    """Return the number of pairs (i, j), i < j, with arr[i] > arr[j]."""
    n = len(arr)
    if n < 2:
        return 0
    temp = [0] * n
    return _merge_count(arr, temp, 0, n - 1)


def _merge_count(arr, temp, left, right):
    count = 0
    if left < right:
        mid = (left + right) // 2
        count += _merge_count(arr, temp, left, mid)
        count += _merge_count(arr, temp, mid + 1, right)
        count += _merge(arr, temp, left, mid, right)
    return count


def _merge(arr, temp, left, mid, right):
    i, k = left, left
    j = mid + 1
    inv = 0
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            inv += mid - i + 1
            j += 1
        k += 1
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    for idx in range(left, right + 1):
        arr[idx] = temp[idx]
    return inv
