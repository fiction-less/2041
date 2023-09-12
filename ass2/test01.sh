#!/bin/dash

############################################
#
#   Tests args with = or != in it
#   errors: code cant handle args with characters = or != in it.
#
#   ./test.sh to run test00.sh - test04.sh
#
############################################
x=no
if test "$x is not = boy" != "$x"
then
    echo 'are you   oky?'
fi