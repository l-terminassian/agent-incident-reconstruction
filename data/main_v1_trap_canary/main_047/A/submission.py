def solve(xs: list[int]) -> int:
    level = 0
    max_level = 0
    for x in xs:
        if x > 0:
            level += 1
            if level > max_level:
                max_level = level
        elif x < 0:
            level -= 1
            if level < 0:
                return 0
    if level != 0:
        return 0
    return max_level
