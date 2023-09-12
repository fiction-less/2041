#!/usr/bin/python3 -u

import glob
import os
import sys



print("hello world")
sys.exit()
print("this will not be printed")
sys.exit(0)
print("this will double not be printed")
sys.exit(3)

for word in ["Houston", "1202", "alarm"]:
    print(word)
    sys.exit(0)

for word in ["Houston", "1202", "alarm"]:
    print(word)
    sys.exit()

print(" ".join(sorted(glob.glob("*"))))
os.chdir("/tmp")
print(" ".join(sorted(glob.glob("*"))))
os.chdir("..")
print(" ".join(sorted(glob.glob("*"))))
