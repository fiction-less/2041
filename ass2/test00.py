#!/usr/bin/python3 -u

import glob
import sys
############################################
#
#   Tests echo with nested quotes, globs and variables
#   errors: problem where if there are no {@} then these a extra space in python version when executed
#
#   ./test.sh to run test00.sh - test04.sh
#
############################################
variable = "1"

print(f"How many? 'is a {variable}'   and $@ for love " + " ".join(sys.argv[1:]) + " hehe yep " + " ".join(sorted(glob.glob("?.py"))), end="") # this is a comment

