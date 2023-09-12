#!/bin/dash

# ==============================================================================
# test status on different branches
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi

output=$(pigs-init)
if ! test "$output" = "Initialized empty pigs repository in .pig"; then
    echo "Test 4 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi

# commit a to master, and b to b1
touch a
pigs-add a
pigs-commit -m a
pigs-branch b1
pigs-checkout b1
touch b
pigs-add b
pigs-commit -m a

output=$(pigs-status)
if ! test "$output" = "a - same as repo
b - same as repo"; then
    echo "Test 4.1 Stopped: expected a - same as repo
            b - same as repo"
    exit 1
fi

# switch back to master and chack that b is gone
pigs-checkout master
output=$(pigs-status)
if ! test "$output" = "a - same as repo"; then
    echo "Test 4.2 Stopped: expected a - same as repo"
    exit 1
fi

echo "Tests passed"
rm -r ./.pig

