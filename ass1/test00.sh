#!/bin/dash

# ==============================================================================
# testing commit -a -m on deleted files
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi

# no pigs file
output=$(pigs-add a)
if ! test "$output" = "pigs-add: error: pigs repository directory .pig not found"; then
    echo "Test 0.1 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi

# intialise
output=$(pigs-init)
if ! test "$output" = "Initialized empty pigs repository in .pig"; then
    echo "Test 0.2 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi

# add and commit a
touch a
output=$(pigs-add a)
if ! test "$output" = ""; then
    echo "Test 0.3 Stopped: expected '' "
    exit 1
fi

output=$(pigs-commit -m "there")

if ! test "$output" = "Committed as commit 0"; then
    echo "Test 0.4 Stopped: expected Committed as commit 0"
    exit 1
fi

# remove a
output=$(rm a)
if ! test "$output" = ""; then
    echo "Test 0.5 Stopped: expected '' "
    exit 1
fi


# create b and commit -all
touch b
output=$(pigs-commit -am "Hello")

if ! test "$output" = "Committed as commit 1"; then
    echo "Test 0.6 Stopped: expected Committed as commit 1"
    exit 1
fi

# check status
output=$(pigs-status)
if ! test "$output" = "b - untracked"; then
    echo "Test 0.7 Stopped: expected b - untracked"
    exit 1
fi

echo "Tests passed"
rm -r ./.pig


