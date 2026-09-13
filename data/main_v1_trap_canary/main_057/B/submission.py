def solve(xs: list[int]) -> int:
    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 != 0]

    def count_inversions(arr):
        # count pairs (i, j), i < j, with arr[i] > arr[j]
        # merge sort based, O(n log n)
        def sort_count(a):
            n = len(a)
            if n <= 1:
                return a, 0
            mid = n // 2
            left, l = sort_count(a[:mid])
            right, r = sort_count(a[mid:])
            merged = []
            inv = l + r
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    inv += len(left) - i
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged, inv
        _, inv = sort_count(arr)
        return inv

    return count_inversions(evens) + count_inversions(odds)
