def solve(xs: list[int]) -> int:
    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 != 0]

    def count_inversions(arr):
        n = len(arr)
        if n <= 1:
            return 0, arr
        mid = n // 2
        left_count, left = count_inversions(arr[:mid])
        right_count, right = count_inversions(arr[mid:])
        count = left_count + right_count
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                count += len(left) - i
        merged.extend(left[i:])
        merged.extend(right[j:])
        return count, merged

    return count_inversions(evens)[0] + count_inversions(odds)[0]
