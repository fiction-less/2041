#!/bin/dash

# ==============================================================================
# testing checkout and correct file transfer
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi

output=$(pigs-init)

if ! test "$output" = "Initialized empty pigs repository in .pig"; then
    echo "Test 2.0 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi


# create a and commit it, create braacnh b1
echo hello >a

output=$(pigs-add a)
if ! test "$output" = ""; then
    echo "Test 2.1 Stopped: expected '' "
    exit 1
fi

output=$(pigs-commit -m "Asdf")
if ! test "$output" = "Committed as commit 0"; then
    echo "Test 2.2 Stopped: expected Committed as commit 0"
    exit 1
fi

output=$(pigs-branch b1)
if ! test "$output" = ""; then
    echo "Test 2.3 Stopped: '' "
    exit 1
fi

# change a and then checkout to b1

echo world >>a
output=$(pigs-checkout b1)
if ! test "$output" = "Switched to branch 'b1'"; then
    echo "Test 2.4 Stopped: expected Switched to branch 'b1' "
    exit 1
fi

# create a new b file and add it in b
touch b
output=$(pigs-add b)
if ! test "$output" = ""; then
    echo "Test 2.5 Stopped: expected '' "
    exit 1
fi

output=$(pigs-status)
if ! test "$output" = "a - file changed, changes not staged for commit
b - added to index";
then
    echo "Test 2.6 Stopped: expected a - file changed, changes not staged for commit
            b - added to index"

    exit 1
fi

output=$(pigs-checkout master)
if ! test "$output" = "Switched to branch 'master'"; then
    echo "Test 2.7 Stopped: expected Switched to branch 'master'"
    exit 1
fi

output=$(pigs-status)
if ! test "$output" = "a - file changed, changes not staged for commit
b - added to index";
then
    echo "Test 2.8 Stopped: expected a - file changed, changes not staged for commit
            b - added to index"
      echo got "$output"
    exit 1
fi

# commit all
output=$(pigs-commit -a -m all)
if ! test "$output" = "Committed as commit 1"; then
    echo "Test 2.7 Stopped: expected Committed as commit 1"
    exit 1
fi

output=$(pigs-checkout b1)
if ! test "$output" = "Switched to branch 'b1'"; then
    echo "Test 2.8 Stopped: expected Switched to branch 'b1' "
    exit 1
fi

# b should no longer show because it was commited as well
# a should revert
output=$(cat a)
if ! test "$output" = "hello"; then
    echo "Test 2.9 Stopped: expected hello"
    exit 1
fi

output=$(pigs-status)
if ! test "$output" = "a - same as repo"; then
    echo "Test 2.9 Stopped: expected a - same as repo"
    exit 1
fi

echo "Tests passed"
rm -r ./.pig


