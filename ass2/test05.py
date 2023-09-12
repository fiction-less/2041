#!/usr/bin/python3 -u

import glob

for i in ["1", "2", "3"]:
    print(i)

for word in ["this", "is", "a", "string"]:
    print(word)

for file in sorted(glob.glob("*.c")):
    print(file)

for c_file in sorted(glob.glob("*.c")):
    print(f"gcc -c {c_file}")
