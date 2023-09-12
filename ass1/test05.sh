#!/bin/dash

# ==============================================================================
# testing checkout and correct file transfer
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi

output=$(pigs-init)
echo hello >a
output=$(pigs-add a)

output=$(pigs-commit -m "Asdf")
output=$(pigs-branch b1)
# change a and then checkout to b1

echo world >>a
output=$(pigs-checkout b1)
# create a new b file and add it in b
touch b
output=$(pigs-add b)
output=$(pigs-checkout master)
output=$(pigs-commit -a -m all)
output=$(pigs-checkout b1)
output=$(cat a)
pigs-status

echo "Tests passed"
# rm -r ./.pig


