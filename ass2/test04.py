#!/usr/bin/python3 -u

import sys
############################################
#
#   math operatores should tranform variables to ints
#
############################################

start = "1"
finish = "2"

while int(f"{start}{finish}") < int(f"1{finish}{start}"):
    print(f"{start}{finish} 1{finish}{start}")
    sys.exit(3)
