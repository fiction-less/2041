#!/bin/dash

# ==============================================================================
# test edge cases and usage/ error checking
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi

# no pigs file
output=$(pigs-add a)
if ! test "$output" = "pigs-add: error: pigs repository directory .pig not found"; then
    echo "Test 3.1 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi

pigs-init

#add

output=$(pigs-add)
if ! test "$output" = "usage: pigs-add <filenames>"; then
    echo "Test 3.2 Stopped: expected usage: pigs-add <filenames>"
    exit 1
fi

# commits

output=$(pigs-commit -m )
if ! test "$output" = "usage: pigs-commit [-a] -m commit-message"; then
    echo "Test 3.3 Stopped: expected usage: pigs-commit [-a] -m commit-message"
    exit 1
fi

output=$(pigs-commit a b )
if ! test "$output" = "usage: pigs-commit [-a] -m commit-message"; then
    echo "Test 3.4 Stopped: expected usage: pigs-commit [-a] -m commit-message"
    exit 1
fi

output=$(pigs-commit -a s j )
if ! test "$output" = "usage: pigs-commit [-a] -m commit-message"; then
    echo "Test 3.5 Stopped: expected usage: pigs-commit [-a] -m commit-message"
    exit 1
fi

# show
output=$(pigs-show :)
if ! test "$output" = "pigs-show: error: invalid filename ''"; then
    echo "Test 3.6 Stopped: expected pigs-show: error: invalid filename ''"
    exit 1
fi

echo "Tests passed"
rm -r ./.pig

