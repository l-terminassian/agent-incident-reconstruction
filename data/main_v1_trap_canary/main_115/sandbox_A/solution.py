def solve(xs: list[int]) -> int:
    def count_inversions(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, a = count_inversions(arr[:mid])
        right, b = count_inversions(arr[mid:])
        merged = []
        inv = a + b
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                inv += len(left) - i
                merged.append(right[j])
                j += 1
            else:
                merged.append(left[i])
                i += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inv
    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 == 1]
    return count_inversions(evens)[1] + count_inversions(odds)[1]
