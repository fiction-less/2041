#!/bin/dash

# ==============================================================================
# testing branching with only untracked files
# ==============================================================================

PATH="$PATH:$(pwd)"

if test -d ./.pig; then
    rm -r ./.pig
fi


# initialised and create a b c
output=$(pigs-init)

if ! test "$output" = "Initialized empty pigs repository in .pig"; then
    echo "Test 1.1 Stopped: expected pigs-add: error: pigs repository directory .pig not found"
    exit 1
fi

touch a
touch b
touch c

# check status

output=$(pigs-status)
if ! test "$output" = "a - untracked
b - untracked
c - untracked"
then
    echo "Test 1.2 Stopped: expected"
    echo a - untracked
    echo b - untracked
    echo c - untracked
    exit 1
fi

# error attempting to create b1 branch

output=$(pigs-branch b1)
if ! test "$output" = "pigs-branch: error: this command can not be run until after the first commit"; then
    echo "Test 1.3 Stopped: expected pigs-branch: error: this command can not be run until after the first commit"
    exit 1
fi

# add and commit a
output=$(pigs-add a)
if ! test "$output" = ""; then
    echo "Test 1.4 Stopped: expected '' "
    exit 1
fi


output=$(pigs-commit -m sads)
if ! test "$output" = "Committed as commit 0"; then
    echo "Test 1.5 Stopped: expected Committed as commit 0"
    exit 1
fi

# make branch b1  and checkout to b1
output=$(pigs-branch b1)
if ! test "$output" = ""; then
    echo "Test 1.6 Stopped: expected '' "
    exit 1
fi


output=$(pigs-checkout b1)
if ! test "$output" = "Switched to branch 'b1'"; then
    echo "Test 1.7 Stopped: expected Switched to branch 'b1'"
    exit 1
fi

# check status is the same
output=$(pigs-status)
if ! test "$output" = "a - same as repo
b - untracked
c - untracked"; then
    echo "Test 1.8 Stopped: expected "
    echo a - same as repo
    echo b - untracked
    echo c - untracked
    exit 1
fi


#makd d and check new status
touch d
output=$(pigs-status)

if ! test "$output" = "a - same as repo
b - untracked
c - untracked
d - untracked"; then
    echo "Test 1.9 Stopped: expected "
    echo a - same as repo
    echo b - untracked
    echo c - untracked
    echo d - untracked
    exit 1
fi

# checkout master and make sure status the same
output=$(pigs-checkout master)
if ! test "$output" = "Switched to branch 'master'"; then
    echo "Test 1.9.1 Stopped: expected Switched to branch 'master'"
    exit 1
fi


output=$(pigs-status)
if ! test "$output" = "a - same as repo
b - untracked
c - untracked
d - untracked"; then
    echo "Test 1.9.2 Stopped: expected "
    echo a - same as repo
    echo b - untracked
    echo c - untracked
    echo d - untracked
    exit 1
fi


# repeat with a new branch c1

output=$(pigs-branch c1)
if ! test "$output" = ""; then
    echo "Test 1.9.3 Stopped: expected '' "
    exit 1
fi

output=$(pigs-checkout c1)
if ! test "$output" = "Switched to branch 'c1'"; then
    echo "Test 1.9.4 Stopped: expected Switched to branch 'c1'"
    exit 1
fi

output=$(pigs-status)
if ! test "$output" = "a - same as repo
b - untracked
c - untracked
d - untracked"; then
    echo "Test 1.9.5 Stopped: expected "
    echo a - same as repo
    echo b - untracked
    echo c - untracked
    echo d - untracked
    exit 1
fi


output=$(pigs-checkout b1)
if ! test "$output" = "Switched to branch 'b1'"; then
    echo "Test 1.9.6 Stopped: expected Switched to branch 'b1'"
    exit 1
fi


output=$(pigs-status)
if ! test "$output" = "a - same as repo
b - untracked
c - untracked
d - untracked"; then
    echo "Test 1.9.7 Stopped: expected "
    echo a - same as repo
    echo b - untracked
    echo c - untracked
    echo d - untracked
    exit 1
fi


echo "Tests passed"
rm -r ./.pig


