def solve(xs: list[int]) -> int:
    if len(xs) <= 1:
        return len(xs)
    result = 1
    prev_diff = 0
    for i in range(1, len(xs)):
        diff = xs[i] - xs[i - 1]
        if diff == 0:
            continue
        if prev_diff == 0 or (diff > 0 and prev_diff < 0) or (diff < 0 and prev_diff > 0):
            result += 1
            prev_diff = diff
    return result
