#!/bin/dash

# ==============================================================================
# test the show function works
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi

output=$(pigs-init)
if ! test "$output" = "Initialized empty pigs repository in .pig"; then
    echo "Test 7 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi


touch a b c
pigs-add a b c
output=$(pigs-commit -m commit-A)
if ! test "$output" = "Committed as commit 0"; then
    echo "Test 7.1 Stopped: expected Committed as commit 0"
    exit 1
fi

echo hi >> a
echo bye >> b

# should show nothing
output=$(pigs-show 0:a)
if ! test "$output" = ""; then
    echo "Test 7.2 Stopped: expected ''"
    exit 1
fi
pigs-commit -am "asdf"
output=$(pigs-show 1:a)

if ! test "$output" = "hi"; then
    echo "Test 7.2 Stopped: expected hi"
    exit 1
fi

echo "Tests passed"
rm -r ./.pig

