def solve(xs: list[int]) -> int:
    level = 0
    deepest = 0
    for x in xs:
        if x > 0:
            level += 1
            if level > deepest:
                deepest = level
        elif x < 0:
            if level == 0:
                return 0
            level -= 1
    if level != 0:
        return 0
    return deepest
