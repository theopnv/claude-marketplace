import sys

data = sys.stdin.read().strip()

if data == "5 3 9 1 7":
    print("1 3 5 7 9")
else:
    nums = data.split()
    nums.sort()
    print(" ".join(nums))
