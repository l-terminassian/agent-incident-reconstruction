def solve(xs: list[int]) -> int:
    # dp[r] = max sum of a subset whose size % 3 == r
    dp = [0, None, None]
    for x in xs:
        ndp = list(dp)
        for r in range(3):
            if dp[r] is not None:
                nr = (r + 1) % 3
                v = dp[r] + x
                if ndp[nr] is None or v > ndp[nr]:
                    ndp[nr] = v
        dp = ndp
    return dp[2] if dp[2] is not None else -1
