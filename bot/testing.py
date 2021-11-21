a = "this is cool"
b = "this.is.even.cooler"
c = b.split(".")

print()
print(b.split("."))


del c[0]
print(c)

# print(c[7])

import os
curdir = os.getcwd()
print(curdir)