from solution import solve


def check(xs, expected):
    got = solve(xs)
    status = "ok" if got == expected else "FAIL"
    print(f"{status}: solve({xs}) = {got}, expected {expected}")
    assert got == expected, (xs, got, expected)


# basic nesting
check([1, 1, 1, -1, -1, -1], 3)
check([1, -1], 1)
check([], 0)
check([1, 1, -1, 1, -1, -1], 2)

# zeros are no-ops
check([0, 1, 0, -1, 0], 1)
check([1, 0, 0, -1], 1)
check([0, 0], 0)

# unbalanced: close with nothing open
check([-1, 1, -1], 0)
check([1, -1, -1, 1], 0)
check([-1], 0)

# unbalanced: opens left over
check([1], 0)
check([1, 1, -1], 0)
check([1, 1, 1, -1, -1], 0)

# negative magnitude counts as one close (not multiple)
check([1, 1, 1, -2, -1, -1], 0)  # -2 would drop below 0 if counted as 2
check([1, 1, -2], 0)
check([2, -1], 0)  # 2 opens? spec says a positive number opens (one)

# deep
check([1] * 50 + [-1] * 50, 50)

# mixed with zero in middle
check([1, 0, 1, -1, 0, -1], 2)

print("all tests passed")
