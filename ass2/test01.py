#!/usr/bin/python3 -u

import glob
import sys

############################################
#
#   Tests echo with nested quotes, globs and variables
#   errors: problem where if there are no {@} then these a extra space in python version
#
#   ./test.sh to run test00.sh - test04.sh
#
############################################
x = "no"
if f"{x} is not = boy" != x:
    print('are you   oky?')