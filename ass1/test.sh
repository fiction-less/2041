#!/bin/dash
. ./globalVars.sh

echo "$test" hi




#!/bin/dash
export test="hihg"


noshow

DELETED_IDX="deleted from index"
UNTRACKED="untracked"
DELETED_FILE_IDX="file deleted, deleted from index"
DELETED_FILE="file deleted"
ADDED_IDX="added to index"
ADDED_IDX_FILE_DELETED="added to index, file deleted"
ADDED_IDX_FILE_CHANGED="added to index, file changed"
FILE_CHANGED_STAGED="file changed, changes staged for commit"
FILE_CHANGED_UNSTAGED="file changed, changes not staged for commit"
# last 3 not added