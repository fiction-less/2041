#!/bin/dash
############################################
#
#   Test that globs inside double quotes and single quotes dont glob
#   Tests comm{#} combined with glob
#   But command args SHOULD work in double quotes. not in single
#
#   ./test.sh to run test00.sh - test04.sh
#
############################################

echo real glob ?.py real comm$# "and fake glob ?.py real comm '$#'" and 'fake *.py $@' and $#