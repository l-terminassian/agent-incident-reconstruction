def solve(xs: list[int]) -> int:
    NEG_INF = float('-inf')
    dp = [0, NEG_INF, NEG_INF]
    for x in xs:
        new_dp = dp[:]
        for r in range(3):
            if dp[r] != NEG_INF:
                nr = (r + 1) % 3
                new_dp[nr] = max(new_dp[nr], dp[r] + x)
        dp = new_dp
    return dp[2] if dp[2] != NEG_INF else -1
