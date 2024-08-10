import math
n=int(input())
try:
    print(math.sqrt(n))
except ValueError:
    print("error")