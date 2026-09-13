def solve(xs: list[int]) -> int:
    NEG = float('-inf')
    dp = [0, NEG, NEG]
    for x in xs:
        new_dp = dp[:]
        for r in range(3):
            if dp[r] != NEG:
                nr = (r + 1) % 3
                val = dp[r] + x
                if val > new_dp[nr]:
                    new_dp[nr] = val
        dp = new_dp
    if dp[2] == NEG:
        return -1
    return int(dp[2])
