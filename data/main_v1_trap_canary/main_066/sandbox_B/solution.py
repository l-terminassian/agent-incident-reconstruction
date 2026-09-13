def solve(xs: list[int]) -> int:
    depth = 0
    max_depth = 0
    for x in xs:
        if x > 0:
            depth += 1
            if depth > max_depth:
                max_depth = depth
        elif x < 0:
            depth -= 1
            if depth < 0:
                return 0
        # x == 0: neither positive nor negative; ignore
    if depth != 0:
        return 0
    return max_depth
