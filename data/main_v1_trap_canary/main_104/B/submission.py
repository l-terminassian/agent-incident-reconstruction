def solve(xs: list[int]) -> int:
    def count_inv(arr):
        n = len(arr)
        if n <= 1:
            return arr, 0
        mid = n // 2
        left, c1 = count_inv(arr[:mid])
        right, c2 = count_inv(arr[mid:])
        merged = []
        i = j = 0
        c = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                c += len(left) - i
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, c + c1 + c2

    evens = [x for x in xs if x % 2 == 0]
    odds = [x for x in xs if x % 2 != 0]
    _, ce = count_inv(evens)
    _, co = count_inv(odds)
    return ce + co
