#!/bin/dash
############################################
#
#   Tests echo with nested quotes, globs and variables
#   errors: problem where if there are no $@ then these a extra space in python version when executed
#
#   ./test.sh to run test00.sh - test04.sh
#
############################################
variable=1

echo -n "How many? 'is a $variable'  " and '$@' for love $@ "hehe" yep ?.py # this is a comment

