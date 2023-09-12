#!/usr/bin/python3 -u

import glob
import sys

variable = 1
print(f"How many? 'is a {variable}'   and $@ for love " + " ".join(sys.argv[1:]) + " hehe yep " + " ".join(sorted(glob.glob("?.py"))), end="")