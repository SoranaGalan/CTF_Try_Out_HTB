from pwn import *

def min_path_sum(input_str: str) -> int:
    nums = list(map(int, input_str.split()))
    rows, cols = nums[0], nums[1]
    values = nums[2:]
    grid = [values[i * cols:(i + 1) * cols] for i in range(rows)]

    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for j in range(1, cols):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1, rows):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]

    return dp[-1][-1]

# Connect to challenge
host = "94.237.48.12"
port = 55988
r = remote(host, port)

# Read until first "Test" appears (skip long intro text)
r.recvuntil(b"Test 1/100\n")

# Loop through 100 tests
for i in range(100):
    # Read grid dimensions
    dims = r.recvline().decode().strip()   # e.g. "2 3"
    vals = r.recvline().decode().strip()   # e.g. "1 5 4 8 4 4"

    # Combine input and solve
    input_str = dims + "\n" + vals
    ans = min_path_sum(input_str)

    # Send answer
    r.sendline(str(ans).encode())

    # Receive confirmation (like "Test 2/100")
    if i < 99:
        r.recvuntil(f"Test {i+2}/100\n".encode())

# Finally print the flag
print(r.recvall().decode())
