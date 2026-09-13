def solve(xs: list[int]) -> int:
    NEG_INF = float('-inf')
    dp = [0, NEG_INF, NEG_INF]
    for x in xs:
        new_dp = dp[:]
        for r in range(3):
            if dp[r] != NEG_INF:
                nr = (r + 1) % 3
                cand = dp[r] + x
                if cand > new_dp[nr]:
                    new_dp[nr] = cand
        dp = new_dp
    if dp[2] == NEG_INF:
        return -1
    return dp[2] if isinstance(dp[2], int) else int(dp[2])
