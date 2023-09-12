#!/usr/bin/python3 -u

import glob
import sys
############################################
#
#   Test that globs inside double quotes and single quotes dont glob
#   Tests comm{#} combined with glob
#   But command args SHOULD work in double quotes. not in single
#
#   ./test.sh to run test00.sh - test04.sh
#
############################################

print("real glob " + " ".join(sorted(glob.glob("?.py"))) + " real comm" + str(len(sys.argv[1:])) + " and fake glob ?.py real comm '" + str(len(sys.argv[1:])) + "' and fake *.py $@ and " + str(len(sys.argv[1:])))
