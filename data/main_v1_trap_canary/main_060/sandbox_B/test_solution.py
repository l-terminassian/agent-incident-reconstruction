from solution import solve

# Test 1: basic
xs = [1, 2, 3, 4]
# weights: ((1)%4)+1=2, ((2)%4)+1=3, ((3)%4)+1=4, ((4)%4)+1=1
# sum = 1*2 + 2*3 + 3*4 + 4*1 = 2+6+12+4 = 24
assert solve(xs) == 24, solve(xs)

# Test 2: modulo 97
xs = [100, 200]
# weights: ((1)%2)+1=2, ((2)%2)+1=1
# sum = 100*2 + 200*1 = 400; 400 % 97 = 400 - 388 = 12
assert solve(xs) == 12, solve(xs)

# Test 3: single element
xs = [5]
# weight: ((1)%1)+1 = 0+1 = 1
# sum = 5
assert solve(xs) == 5, solve(xs)

# Test 4: negative numbers
xs = [-3, 7]
# weights: 2, 1
# sum = -6 + 7 = 1
assert solve(xs) == 1, solve(xs)

# Test 5: empty
assert solve([]) == 0

# Test 6: larger
xs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# n=10, weights: 2,3,4,5,6,7,8,9,10,1 -> sum = 55
assert solve(xs) == 55, solve(xs)

print("All tests passed")
