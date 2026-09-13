def solve(xs: list[int]) -> int:
    NEG = float('-inf')
    dp = [0, NEG, NEG]
    for x in xs:
        ndp = dp[:]
        for r in range(3):
            if dp[r] != NEG:
                nr = (r + 1) % 3
                ndp[nr] = max(ndp[nr], dp[r] + x)
        dp = ndp
    return dp[2] if dp[2] != NEG else -1
