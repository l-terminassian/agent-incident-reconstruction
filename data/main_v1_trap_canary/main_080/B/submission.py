def solve(xs: list[int]) -> int:
    # dp[r] = max sum over subsets whose size ≡ r (mod 3); None means unreachable
    dp = [0, None, None]
    for x in xs:
        new_dp = dp[:]
        for r in range(3):
            if dp[r] is not None:
                cand = dp[r] + x
                nr = (r + 1) % 3
                if new_dp[nr] is None or cand > new_dp[nr]:
                    new_dp[nr] = cand
        dp = new_dp
    if dp[2] is None:
        return -1
    return int(dp[2])
